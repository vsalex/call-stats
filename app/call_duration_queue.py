from datetime import datetime, timedelta

from app.models import Call, Duration


class CallDurationQueue(object):
    def __init__(self):
        self.calls = []
        self.duration = []

    def add_object(self, _obj):
        """
        Add object to DailyStat. From here can be few options:
        1. New Call or Duration object will be added to self.calls or
        self.duration list and will wait for opposite object with same call_id
        to refresh stats.
        2. If new Call or Duration object will find opposite object with same
        call id it will refresh daily stats.

        :param _obj: <object> Call or Duration
        :return: True if object added and None otherwise
        """

        result_of_adding = {}

        # First of all lets check all our messages if any outdated here. In
        # production this method my be called every second, but it depends
        # of self.calls and self.duration size - if there will be 1 000 000
        # objects it can be wasteful, anyway this shall be designed based on
        # real case.
        checking_result = self._check_outdated_messages()
        if checking_result:
            result_of_adding.update(checking_result)

        # Set start of object processing datetime to define when it will be
        # outdated. Depends on real case creation time can be set when Call
        # or Duration object are initialized or at the moment of adding into
        # self.calls or self.duration i think.
        _obj.entry_time = datetime.now()

        if isinstance(_obj, Call):
            matching_result = self._match(_obj, self.calls, self.duration)
        elif isinstance(_obj, Duration):
            matching_result = self._match(_obj, self.duration, self.calls)
        else:
            raise NameError("Error! Found some unexpected object %s in "
                              "CallDurationQueue!" % _obj)

        if matching_result:
            result_of_adding.update(matching_result)

        return result_of_adding

    def _match(self, _obj, _obj_list, another_list):
        another_obj = self._get_elem_by_call_id(another_list, _obj.call_id)
        if another_obj:
            another_list.remove(another_obj)
            return {
                "matched": {
                    _obj.__class__.__name__.lower(): _obj,
                    another_obj.__class__.__name__.lower(): another_obj,
            }}
        else:
            _obj_list.append(_obj)

        return False

    @staticmethod
    def _get_elem_by_call_id(_list, call_id):
        """
        Return Call or Duration object from _list by call_id.

        :param _list: <list> of Call or Duration objects
        :param call_id: <int>
        :return: <object> from _list or None
        """

        for elem in _list:
            if elem.call_id == call_id:
                return elem

        return None


    @staticmethod
    def _remove_outdated_from_list(_list, _hours=24):
        """
        Remove outdated Call or Duration object from self.calls or
        self.duration lists.

        :param _list: <list> self.calls or self.duration
        :param _hours: <int> number of hours in which Call or Duration object
        will be outdated
        :return: <int> number of removed objects from _list
        """

        removed_elements = []
        for elem in _list:
            if (elem.entry_time + timedelta(hours=_hours)) < datetime.now():
                removed_elements.append(elem)
                _list.remove(elem)

        return removed_elements

    def _check_outdated_messages(self):
        """
        Check self.calls and self.duration lists for outdated elements (default
        is 24 hours). And if we have some, then increase appropriate stats.
        """

        removed_calls = self._remove_outdated_from_list(self.calls)
        if removed_calls:
            return {"outdated_calls": removed_calls}

        removed_duration = self._remove_outdated_from_list(self.duration)
        if removed_duration:
            return {"outdated_durations": removed_duration}