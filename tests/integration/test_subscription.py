import pytest
from services import subscription
from unittest.mock import Mock


pytest_plugins = [
    "tests.integration.fixtures",
]


def test_register(
        registration_input,
        user_repository,
        user_notifier,
        account_uuid,
        email):
    user_repository.create_file_store = Mock(
        side_effect=user_repository.create_file_store)
    subscription.register(registration_input, user_repository, user_notifier)
    user_repository.create_file_store.assert_called_once_with(account_uuid)
    registered_user = user_repository.get_user_by_id(account_uuid)
    assert registered_user.email == email


def test_authentication_success(
        user_repository,
        email,
        password,
        account_uuid):
    user_input = {"email": email, "password": password}
    authenticated_user = subscription.authenticate(user_input, user_repository)
    assert authenticated_user.identifier == account_uuid


def test_authentication_failure(user_repository):
    user_input = {
        "email": "random_email@vueshot.com",
        "password": "incorrect_password"}
    with pytest.raises(subscription.AuthenticationFailed):
        subscription.authenticate(user_input, user_repository)
