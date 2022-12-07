import json
import logging
from vue import repository, logs

logger = logging.getLogger('entrypoint.api.rec')


def store_screencast(dir_path: str, chunk: bytearray,
                     report_repo: repository.AbstractReportRepository):
    report_repo.store_screencast_chunks(dir_path, chunk)


class InvalidLog(Exception):
    pass


def store_console_log_entry(report_id: str,
                            user_id: str,
                            entry_details: dict,
                            report_repo: repository.AbstractReportRepository):
    if "entry" not in entry_details:
        raise InvalidLog("No entry found in Console Log")

    if entry_details["entry"] is None:
        raise InvalidLog("Invalid Console Log")

    try:
        log_request = entry_details["entry"]
        console_log = logs.ConsoleLogEntry(log_request)
    except Exception as err:
        logger.error(err)
        raise InvalidLog("Trouble unpacking console log data")

    if console_log is None:
        raise InvalidLog("Invalid Console Log")

    report_repo.store_console_log(report_id, user_id, console_log)


def store_network_log_entry(report_id: str,
                            user_id: str,
                            net_log_record: dict,
                            report_repo: repository.AbstractReportRepository):
    if "requestId" not in net_log_record:
        raise InvalidLog("Invalid Network Log")

    try:
        network_log = logs.NetworkLogEntry(net_log_record)
    except Exception as err:
        logger.error(err)
        raise InvalidLog("Trouble unpacking network log data")

    if network_log is None:
        raise InvalidLog("Invalid Network Log")

    report_repo.store_network_log(report_id, user_id, network_log)
