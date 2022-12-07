import json


class ConsoleLogEntry:

    def __init__(self, dictionary=None):
        self._level = None
        self._source = None
        self._text = None
        self._url = None
        self._timestamp = None
        self._record = None

        if dictionary is not None:
            for key, value in dictionary.items():
                attr_name = f"_{key}"
                if not hasattr(self, attr_name):
                    continue
                setattr(self, attr_name, value)

            self._record = json.dumps(dictionary)

    @property
    def level(self):
        return self._level

    @property
    def source(self):
        return self._source

    @property
    def text(self):
        return self._text

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def url(self):
        return self._url

    @property
    def record(self):
        return self._record

    @level.setter
    def level(self, level):
        self._level = level

    @source.setter
    def source(self, source):
        self._source = source

    @text.setter
    def text(self, text):
        self._text = text

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = timestamp

    @url.setter
    def url(self, url):
        self._url = url

    @record.setter
    def record(self, record):
        self._record = record


class NetworkLogEntry:

    def __init__(self, dictionary=None):
        self._request_id = None
        self._method = None
        self._timestamp = None
        self._record = None
        self._resource_type = None
        self._resource_url = None
        self._walltime = None

        if dictionary is not None:
            for key, value in dictionary.items():
                attr_name = f"_{key}"
                if not hasattr(self, attr_name):
                    continue
                setattr(self, attr_name, value)

            self._request_id = dictionary["requestId"]
            if "type" in dictionary:
                self._resource_type = dictionary["type"]

            if "wallTime" in dictionary:
                self._walltime = dictionary["wallTime"]

            if "documentURL" in dictionary:
                self._resource_url = dictionary["documentURL"]

            self._record = json.dumps(dictionary)

    @property
    def request_id(self):
        return self._request_id

    @property
    def method(self):
        return self._method

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def record(self):
        return self._record

    @property
    def resource_type(self):
        return self._resource_type

    @property
    def resource_url(self):
        return self._resource_url

    @property
    def walltime(self):
        return self._walltime

    @request_id.setter
    def request_id(self, request_id):
        self._request_id = request_id

    @method.setter
    def method(self, method):
        self._method = method

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = timestamp

    @record.setter
    def record(self, record):
        self._record = record

    @resource_type.setter
    def resource_type(self, resource_type):
        self._resource_type = resource_type

    @resource_url.setter
    def resource_url(self, resource_url):
        self._resource_url = resource_url

    @walltime.setter
    def walltime(self, walltime):
        self._walltime = walltime


class Payload:

    def __init__():
        self._request_id = None
        self._request = None
        self._response = None
        # based on responseReceived or loadingFailed or nothing received
        self._successful = False
        # if either responseReceived or loadingFailed has been received
        self._complete = False
        self._duration = None
        # Fetch or XHR
        self._api_type = None
