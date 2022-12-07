import abc


class User:
    def __init__(self):
        self.email = None
        self.name = None
        self.password = None
        self.identifier = None

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def identifier(self):
        return self._identifier

    @property
    def password(self):
        return self._password

    @name.setter
    def name(self, name):
        self._name = name

    @email.setter
    def email(self, email):
        self._email = email

    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    @password.setter
    def password(self, password):
        self._password = password

    def __str__(self):
        return f"{self._name}({self._email})"


class AbstractUserNotification(abc.ABC):
    @abc.abstractmethod
    def notify_user(person: User):
        raise NotImplementedError
