import os
import io
import logging
import psycopg
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from vue import repository, report, logs
from identity import gen
from typing import List

logger = logging.getLogger('entrypoint.api.rpt')


class InvalidTimezone(Exception):
    pass


class InvalidReport(Exception):
    pass


class ReportRepository(repository.AbstractReportRepository):

    def __init__(self, pool: ConnectionPool):
        self.pool = pool
        self._chunk_queue = dict()
        self._store_offset = dict()

    def _get_timezone_details(self, tz: str) -> dict:
        conn = self.pool.getconn()
        cur = conn.cursor(row_factory=dict_row)
        try:
            tz_details = cur.execute(
                "SELECT * FROM pg_timezone_names where name = %s", (tz,)).fetchone()
        except (Exception) as err:
            logger.error(err)
            raise Exception
        finally:
            self.pool.putconn(conn)

        return tz_details

    def store_report(self, rpt: report.Report) -> str:
        conn = self.pool.getconn()
        conn.autocommit = False
        tx = conn.transaction()
        tx.isolation_level = psycopg.IsolationLevel(2)
        cur = conn.cursor()
        try:
            tz_dets = self._get_timezone_details(rpt.timezone)
            if tz_dets is None:
                raise InvalidTimezone("Invalid timezone value")

            random_uuid = gen.get_uuid()

            utc_offset = tz_dets["utc_offset"]
            is_dst = tz_dets["is_dst"]

            cur.execute(
                '''INSERT INTO report(report_uuid, account_uuid, locale, timezone,
            timezone_offset, tz_daylight_savings, has_timezone_data,
            record_console_log_requested, record_network_log_requested) VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (random_uuid,
                 rpt.creator,
                 rpt.locale,
                 rpt.timezone,
                 utc_offset,
                 is_dst,
                 True,
                 rpt.has_console_log,
                 rpt.has_network_log))
            conn.commit()
        except (Exception) as err:
            logger.error(err)
            conn.rollback()
            raise err
        finally:
            conn.autocommit = True
            self.pool.putconn(conn)
        return random_uuid

    def create_file_store(self, rpt: report.Report):
        if rpt is None:
            raise InvalidReport("Invalid Report")

        if rpt.identifier is None or rpt.creator is None:
            raise InvalidReport("Invalid Report")

        user_id = rpt.creator.strip()
        report_id = rpt.identifier.strip()

        if len(user_id) == 0 or len(report_id) == 0:
            raise InvalidReport("Invalid Ids in the Report")

        try:
            dir_path = f"./{user_id}/{report_id}"
            os.mkdir(dir_path)
        except Exception as err:
            logger.error("Error creating directory for " + dir_path, err)
            raise err

    def store_screencast_chunks(self, dir_path: str, chunk: bytearray):
        if dir_path in self._chunk_queue:
            self._chunk_queue[dir_path].append(chunk)
            chunks = self._chunk_queue[dir_path]
            if len(chunks) == 20:
                offset = self._store_offset[dir_path]
                num = int(offset) + 1
                filename = f"{dir_path}/part_{num}"
                with open(filename, 'ab') as fn:
                    for chunk in chunks:
                        fn.write(chunk)

                self._store_offset[dir_path] = num
                self._chunk_queue[dir_path].clear()
            return

        _chunks = list()
        _chunks.append(chunk)
        self._chunk_queue[dir_path] = _chunks
        self._store_offset[dir_path] = 0
        return

    def aggregate_screencast_chunks(self, dir_path: str):
        chunks = self._chunk_queue[dir_path]
        offset = self._store_offset[dir_path]
        num = int(offset) + 1
        filename = f"{dir_path}/part_{num}"
        with open(filename, 'ab') as fn:
            for chunk in chunks:
                fn.write(chunk)

        self._store_offset[dir_path] = num
        self._chunk_queue[dir_path].clear()

        consolidated_file = open(f"{dir_path}/rec.webm", 'ab')
        for part_index in range(1, num + 1):
            part_filename = open(f"{dir_path}/part_{part_index}", 'rb')
            contents = part_filename.read()
            consolidated_file.write(contents)
            part_filename.close()
        consolidated_file.close()

    def store_console_log(
            self,
            report_id: str,
            user_id: str,
            console: logs.ConsoleLogEntry):
        conn = self.pool.getconn()
        conn.autocommit = False
        tx = conn.transaction()
        tx.isolation_level = psycopg.IsolationLevel(2)
        cur = conn.cursor()

        try:
            cur.execute(
                '''INSERT INTO console_log_entry(report_uuid, account_uuid,
            log_level, log_source, log_text, entry_timestamp, log_url, entry_record) VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)''',
                (report_id,
                 user_id,
                 console.level,
                 console.source,
                 console.text,
                 console.timestamp,
                 console.url,
                 console.record))
            conn.commit()
        except (Exception) as err:
            logger.error(err)
            conn.rollback()
            raise err
        finally:
            conn.autocommit = True
            self.pool.putconn(conn)

    def store_network_log(
            self,
            report_id: str,
            user_id: str,
            network: logs.NetworkLogEntry):
        conn = self.pool.getconn()
        conn.autocommit = False
        tx = conn.transaction()
        tx.isolation_level = psycopg.IsolationLevel(2)
        cur = conn.cursor()

        try:
            cur.execute(
                '''INSERT INTO network_log_entry(report_uuid, account_uuid, request_id,
            resource_type, resource_url, network_event, entry_timestamp, entry_wall_time, entry_record) VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (report_id,
                 user_id,
                 network.request_id,
                 network.resource_type,
                 network.resource_url,
                 network.method,
                 network.timestamp,
                 network.walltime,
                 network.record))
            conn.commit()
        except (Exception) as err:
            logger.error(err)
            conn.rollback()
            raise err
        finally:
            conn.autocommit = True
            self.pool.putconn(conn)

    def get_network_payload(self, report_id: str) -> List[logs.Payload]:
        # select distinct req.request_id, req.resource_type, req.network_event, req.entry_timestamp, req.entry_record,
        # res.request_id, res.resource_type, res.network_event, res.entry_timestamp, res.entry_record
        # from public.network_log_entry req inner join public.network_log_entry res
        # on req.request_id = res.request_id and req.entry_timestamp <
        # res.entry_timestamp and req.report_uuid =
        # '69c58d61e0c246eb9b330972e2947ef3' order by req.request_id

        # select request_id, resource_type, network_event, entry_record from public.network_log_entry
        # where request_id in (select request_id from public.network_log_entry where report_uuid = '69c58d61e0c246eb9b330972e2947ef3'
        # group by request_id having count(request_id) = 1 order by request_id)
        pass

    def get_console_log_entries(self,
                                report_id: str) -> List[logs.ConsoleLogEntry]:
        pass
