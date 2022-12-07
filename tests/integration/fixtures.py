import pytest
from vue import repository, user


class FakeUserRepository(repository.AbstractUserRepository):

    def __init__(self):
        self.users = {}

    def create_user_account(self, person: user.User) -> str:
        uuid = "b79c73eeee48585ec20380177d580gbc"
        user_record = {
            "account_uuid": uuid,
            "full_name": person.name,
            "email": person.email,
            "pass": person.password}
        self.users[person.email] = user_record
        return uuid

    def create_file_store(self, user_account_id: str):
        return

    def get_user_by_email(
            self,
            email: str,
            with_password: bool = False) -> user.User:
        existing_user = None
        if email not in self.users:
            return existing_user

        user_record = self.users[email]
        existing_user = user.User()
        existing_user.identifier = user_record["account_uuid"]
        existing_user.email = email
        existing_user.name = user_record["full_name"]
        if with_password:
            existing_user.password = user_record["pass"]

        return existing_user

    def get_user_by_id(self, id: str) -> user.User:
        existing_user = None
        for key in self.users:
            user_record = self.users[key]
            if user_record["account_uuid"] == id:
                existing_user = user.User()
                existing_user.identifier = id
                existing_user.email = key
                existing_user.name = user_record["full_name"]
                return existing_user

        return existing_user


class FakeNotification(user.AbstractUserNotification):

    def notify_user(person: user.User):
        pass


@pytest.fixture()
def account_uuid():
    uuid = "b79c73eeee48585ec20380177d580gbc"
    return uuid


@pytest.fixture()
def registration_input():
    user_input = {
        "email": "test@vueshot.com",
        "fullname": "Fake User",
        "password": "P@55w00rd9765_vs",
        "confirm": "P@55w00rd9765_vs"
    }

    return user_input


@pytest.fixture()
def email():
    return "test@vueshot.com"


@pytest.fixture()
def password():
    return "P@55w00rd9765_vs"


@pytest.fixture(scope="module")
def user_repository():
    repo = FakeUserRepository()
    return repo


@pytest.fixture(scope="module")
def user_notifier():
    notifier = FakeNotification()
    return notifier
