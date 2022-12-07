import bcrypt
import re
import socket
import logging
from vue import repository, user, report

logger = logging.getLogger('entrypoint.api.sub')


class InvalidEmailFormat(Exception):
    pass


class InvalidEmailHost(Exception):
    pass


class PassConfirmMismatch(Exception):
    pass


class NonUniqueEmail(Exception):
    pass


def register(registration_input: dict,
             repo: repository.AbstractUserRepository,
             notifier: user.AbstractUserNotification):
    user_registration_input = unpack_registration_input(registration_input)
    name, email, password, confirm = user_registration_input

    if password != confirm:
        raise PassConfirmMismatch(
            "Password and Confirm Password are not matching")

    email = get_punycode(email)

    # check if email has valid format and is actually a valid email
    if not is_valid_format(email):
        raise InvalidEmailFormat("Invalid email format")

    if not is_valid_host(email):
        raise InvalidEmailHost("Invalid email host")

    existing_user = repo.get_user_by_email(email)
    if existing_user:
        raise NonUniqueEmail("Email already exists")

    hashed_password = get_hashed_pass(password)
    str_password = hashed_password.decode('utf-8')

    person = user.User()
    person.email = email
    person.name = name
    person.password = str_password

    user_id = repo.create_user_account(person)
    # TODO send an email with a verification link and only if it is confirmed
    # create a file store for the video file parts
    repo.create_file_store(user_id)
    return


class EmptyInput(Exception):
    pass


class AuthenticationFailed(Exception):
    pass


def unpack_registration_input(input: dict) -> tuple:
    if "email" not in input:
        raise EmptyInput("Email field is empty")

    if "fullname" not in input:
        raise EmptyInput("Fullname field is empty")

    if "password" not in input:
        raise EmptyInput("Password field is empty")

    if "confirm" not in input:
        raise EmptyInput("Confirm password field is empty")

    email = input["email"].strip()
    if len(email) == 0:
        raise EmptyInput("Email field is empty")

    name = input["fullname"].strip()
    if len(name) == 0:
        raise EmptyInput("Fullname field is empty")

    password = input["password"].strip()
    if len(password) == 0:
        raise EmptyInput("Password field is empty")

    confirm = input["confirm"].strip()
    if len(confirm) == 0:
        raise EmptyInput("Confirm password field is empty")

    user_registration_data = (name, email, password, confirm)
    return user_registration_data

# Returns Punycode representation of the internationalized domain name
# e.g., 中国.asia is converted to xn--fiqs8s.asia
# source:
# https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DomainNameFormat.html#domain-name-format-idns


def get_punycode(email: str) -> str:
    punycode_str = email.lower().encode('idna').decode('UTF-8')
    return punycode_str


def is_valid_format(email: str) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    return False


def is_valid_host(email: str) -> bool:
    email_parts = email.split('@')
    host_name = email_parts[1]
    try:
        address = socket.gethostbyname(host_name)
        if address:
            return True
    except Exception as err:
        logger.error(err)
        return False


def get_hashed_pass(password: str) -> str:
    byte_password = password.encode('utf-8')
    password_salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(byte_password, password_salt)
    return hashed_pass


def unpack_auth_input(input: dict) -> tuple:
    if "email" not in input:
        raise EmptyInput("Email field is empty")

    if "password" not in input:
        raise EmptyInput("Password field is empty")

    email = input["email"].strip()
    if len(email) == 0:
        raise EmptyInput("Email field is empty")

    password = input["password"].strip()
    if len(password) == 0:
        raise EmptyInput("Password field is empty")

    user_authentication_data = (email, password)
    return user_authentication_data


def authenticate(auth_input: dict,
                 repo: repository.AbstractUserRepository) -> user.User:

    user_authentication_input = unpack_auth_input(auth_input)
    email, password = user_authentication_input

    if not is_valid_format(email):
        raise InvalidEmailFormat("Invalid email format")

    existing_user = repo.get_user_by_email(email, with_password=True)
    if not existing_user:
        raise AuthenticationFailed("Incorrect username or password")

    str_password = existing_user.password
    b_password = bytes(str_password, 'utf-8')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), b_password)

    if hashed_password != b_password:
        raise AuthenticationFailed("Incorrect username or password")

    existing_user.password = None
    return existing_user
