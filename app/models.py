import re
from datetime import datetime

import app.utils as utils


class DailyStatObj(object):
    """
    Base abstract class for Calls and duration.
    """

    def __init__(self):
        """
        Object entry_time attribute is used for time until this call is
        relevant (not outdated). It will set after putting into queue.
        """

        self.errors = []
        self.entry_time = None

    def _set_call_id(self, call_id, call_id_format):
        """
        Check call_id for correct type.

        :param call_id: <str>
        :param call_id_format: <type>
        """

        if isinstance(call_id, call_id_format):
            self.call_id = call_id
        else:
            self.call_id = False
            self.errors.append(
                "Can't set call id %s, because of format. It must be %s, but "
                "now it is %s!" % (call_id, call_id_format, type(call_id)))


class Call(DailyStatObj):
    """
    Call object. Matches timestamp, source_number and dest_number during object
    creation by correct formats.
    """

    def __init__(self, call_id, timestamp, source_number, dest_number):
        """
        Trying to initialize Call object. If something wrong - add some errors
        which are available by obj.errors attribute.
        """

        super().__init__()

        self._set_call_id(call_id, utils.call_id_format)
        self._set_timestamp(timestamp, utils.timestamp_format)
        self._set_number("source_number", source_number, utils.number_format)
        self._set_number("dest_number", dest_number, utils.number_format)

    def _set_timestamp(self, timestamp, timestamp_format):
        """
        Sets timestamp attribute for Call object if current timestamp have
        correct format.

        :param timestamp: <str> timestamp.
        :param timestamp_format: <str> ISO 8601 formatted datetime string.
        """

        try:
            self.timestamp = datetime.strptime(timestamp, timestamp_format)
        except ValueError as e:
            self.timestamp = False
            self.errors.append(
                "Can't read timestamp! Timestamp: %s, format: %s" %
                (timestamp, timestamp_format))

    def _set_number(self, obj_attr_name, number, number_format):
        """
        Sets object attribute obj_attr_name if number matches number_format.

        :param obj_attr_name: <str> object attribute name which will be set if
        number have correct format.
        :param number: <str> number that was passed from __init__ method.
        :param number_format: <str> number format that matches number.
        """

        if re.compile(number_format).match(number):
            setattr(self, obj_attr_name, number)
        else:
            setattr(self, obj_attr_name, False)
            self.errors.append(
                "Can't read number: %s! Number is: %s, format: %s" %
                (obj_attr_name, number, number_format))

    def __repr__(self):
        return "Call {0} timestamp: {1}, from {2} to {3}".format(
            self.call_id, self.timestamp, self.source_number, self.dest_number,
        )


class Duration(DailyStatObj):
    """
    Duration object. Matches call_id and duration during object creation by
    correct formats.
    """

    def __init__(self, call_id, duration):
        """
        Object entry_time attribute is used for time until this call is
        relevant (not outdated). It will set after putting into queue.
        """

        super().__init__()

        self._set_call_id(call_id, utils.call_id_format)
        self._set_duration(duration, utils.duration_format)

    def _set_duration(self, duration, duration_format):
        """
        Check duration for correct type.

        :param duration: <str>
        :param duration_format: <type>
        """

        if isinstance(duration, duration_format):
            self.duration = duration
        else:
            self.duration = False
            self.errors.append(
                "Can't set duration of call %s, because of format. It must be "
                "%s, but now it is %s!" %
                (duration, duration_format, type(duration)))

    def __repr__(self):
        return "Duration {0}: {1} sec(s)".format(self.call_id, self.duration)
