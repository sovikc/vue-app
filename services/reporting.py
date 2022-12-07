import logging
from vue import repository, report

logger = logging.getLogger('entrypoint.api.rep')


def create_report(
        record_request: dict,
        report_repo: repository.AbstractReportRepository,
        user_repo: repository.AbstractUserRepository) -> report.Report:
    if not is_recording_initiation_call(record_request):
        raise UnkownInitiationRequest("Unkown payload in recording initiation")

    rpt = unpack_record_dets(record_request)

    person = user_repo.get_user_by_id(rpt.creator)
    if person is None:
        raise UnauthorizedInitiationRequest("No valid user found")

    report_uuid = report_repo.store_report(rpt)

    is_invalid_uuid = report_uuid is None or len(report_uuid.strip()) == 0
    if is_invalid_uuid:
        raise InvalidReport("Report couldn't be created")

    rpt.identifier = report_uuid
    report_repo.create_file_store(rpt)

    return rpt


def consolidate_recordings(
        dir_path: str,
        report_repo: repository.AbstractReportRepository):
    report_repo.aggregate_screencast_chunks(dir_path)

    # 1. fetch network logs for the report from db and aggregate them using
    # the domain object
    report_id = get_report_id(dir_path)
    # TODO
    # payload_list = report_repo.get_network_payload(report_id)
    # 2. store the network payload in a log file
    # 3. fetch console logs
    # 4. store the console log in a log file
    # 5. update the log file locations in the report table
    # 6. delete console and network log entries from db


class UnauthorizedInitiationRequest(Exception):
    pass


class UnkownInitiationRequest(Exception):
    pass


class InvalidReport(Exception):
    pass


def unpack_record_dets(record_request: dict) -> report.Report:
    req = record_request["value"]
    initial_call = req["call"]
    user_id = req["userID"]

    if user_id is None:
        raise UnauthorizedInitiationRequest("No valid user found")

    user_id = user_id.strip()
    if len(user_id) == 0:
        raise UnauthorizedInitiationRequest("No valid user found")

    call_data = req["data"]
    if call_data is None:
        raise UnkownInitiationRequest(
            "Invalid payload in recording initiation")

    rpt = report.Report.skinny_instance(user_id, call_data)
    return rpt


def is_recording_initiation_call(record_request: dict) -> bool:
    if "value" not in record_request.keys():
        return False

    req = record_request["value"]
    if "call" not in req:
        return False

    initial_call = req["call"]
    if initial_call != "connect":
        return False

    return True


def get_report_id(dir_path: str) -> str:
    dir_path_parts = dir_path.split('/')

    report_id = dir_path_parts[-1]
    if report_id is None:
        logger.error("Report Id couldn't be retrieved from dir_path")
        raise ValueError("Report Id couldn't be retrieved from dir_path")

    report_id = report_id.strip()
    if len(report_id) == 0:
        logger.error("Report Id retrieved from dir_path is empty")
        raise ValueError("Report Id retrieved from dir_path is empty")
    return report_id
