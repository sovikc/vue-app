class Report:

    @property
    def identifier(self):
        return self._identifier

    @property
    def creator(self):
        return self._creator_id

    @property
    def label(self):
        return self._label

    @property
    def locale(self):
        return self._locale

    @property
    def timezone(self):
        return self._timezone

    @property
    def has_console_log(self):
        return self._has_console_log

    @property
    def has_network_log(self):
        return self._has_network_log

    @property
    def tz_offset(self):
        return self._tz_offset

    @property
    def description(self):
        return self._description

    @property
    def tab_capture_location(self):
        return self._tab_capture_location

    @property
    def audio_location(self):
        return self._audio_location

    @property
    def ip_address(self):
        return self._ip_address

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    @creator.setter
    def creator(self, creator):
        self._creator_id = creator

    @label.setter
    def label(self, label):
        self._label = label

    @locale.setter
    def locale(self, locale):
        self._locale = locale

    @timezone.setter
    def timezone(self, timezone):
        self._timezone = timezone

    @has_console_log.setter
    def has_console_log(self, has_console_log):
        self._has_console_log = has_console_log

    @has_network_log.setter
    def has_network_log(self, has_network_log):
        self._has_network_log = has_network_log

    @tz_offset.setter
    def tz_offset(self, tz_offset):
        self._tz_offset = tz_offset

    @description.setter
    def description(self, description):
        self._description = description

    @tab_capture_location.setter
    def tab_capture_location(self, tab_capture_location):
        self._tab_capture_location = tab_capture_location

    @audio_location.setter
    def audio_location(self, audio_location):
        self._audio_location = audio_location

    @ip_address.setter
    def ip_address(self, ip_address):
        self._ip_address = ip_address

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @end_time.setter
    def end_time(self, end_time):
        self._end_time = end_time

    @staticmethod
    def skinny_instance(user_id: str, dictionary: dict):
        if user_id is None or dictionary is None:
            raise ValueError("Error creating Report")

        rpt = Report()
        rpt.creator = user_id
        rpt.locale = dictionary["locale"]
        rpt.timezone = dictionary["timezone"]
        rpt.has_console_log = dictionary["storeConsoleLog"]
        rpt.has_network_log = dictionary["storeNetworkLog"]

        return rpt

    def __str__(self):
        return f"{self._label}({self._identifier})"
