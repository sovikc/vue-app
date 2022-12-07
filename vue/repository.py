import abc
from vue import user, report, logs
from typing import List


class AbstractUserRepository(abc.ABC):
    @abc.abstractmethod
    def create_user_account(person: user.User) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def create_file_store(user_account_id: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_email(
            email: str,
            with_password: bool = False) -> user.User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_id(id: str) -> user.User:
        raise NotImplementedError


class AbstractReportRepository(abc.ABC):
    @abc.abstractmethod
    def store_report(rpt: report.Report) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def create_file_store(rpt: report.Report):
        raise NotImplementedError

    @abc.abstractmethod
    def store_screencast_chunks(dir_path: str, chunk: bytearray):
        raise NotImplementedError

    @abc.abstractmethod
    def aggregate_screencast_chunks(dir_path: str):
        raise NotImplementedError

    @abc.abstractmethod
    def store_console_log(
            report_id: str,
            user_id: str,
            console: logs.ConsoleLogEntry):
        raise NotImplementedError

    @abc.abstractmethod
    def store_network_log(
            report_id: str,
            user_id: str,
            network: logs.NetworkLogEntry):
        raise NotImplementedError

    @abc.abstractmethod
    def get_network_payload(report_id: str) -> List[logs.Payload]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_console_log_entries(report_id: str) -> List[logs.ConsoleLogEntry]:
        raise NotImplementedError
