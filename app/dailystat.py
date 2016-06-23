import re

import app.utils as utils


class DailyStat(object):
    def __init__(self, current_date):
        self.current_date = current_date

        # общее количество звонков
        self.summary_number_of_calls = 0

        # суммарная длительность звонков
        self.summary_calls_duration = 0

        # кол-во звонков по каждому телефонному коду
        self.number_of_calls_by_code = {}

        # сумарная длительлность по каждому телефонному коду
        self.summary_duration_by_code = {}

        # кол-во несматченных сообщений из очереди Call
        self.do_not_matched_calls = 0

        # кол-во несматченных сообщений из очереди Duration
        self.do_not_matched_duration = 0

    @staticmethod
    def _get_code_from_phone(phone_number):
        """
        Returns phone code from phone number.

        :param phone_number: <str> source or dest phone number.
        """

        result = re.search(utils.code_number_format, phone_number)
        if result:
            return result.group(0)
        else:
            # Here must be some logging in production
            print("Error! Can't find phone code %s in %s!" %
                  (utils.code_number_format, phone_number))

    @staticmethod
    def _get_attribute_by_name(obj1, obj2, attribute_name):
        """
        Returns value of searched attribute from obj1 or obj2 (depend on where
        search attribute will be find).

        :param obj1: <object> Call or Duration.
        :param obj2: <object> Call or Duration.
        :param attribute_name: <str> name of searched attribute.
        :return: value of searched attribute.
        """

        if hasattr(obj1, attribute_name):
            return getattr(obj1, attribute_name)
        elif hasattr(obj2, attribute_name):
            return getattr(obj2, attribute_name)
        else:
            # Here must be some logging in production
            print(
                "Error during checking queues! %s and %s doesn't has attribute"
                " %s" % (obj1, obj2, attribute_name))

    def _increase_number_of_calls_by_code(self, obj1, obj2, number_type):
        """
        Increases number of calls by specific code in
        self.number_of_calls_by_code dict.

        :param obj1: <object> Call or Duration.
        :param obj2: <object> Call or Duration.
        :param number_type: <str> source_number or dest_number.
        """

        number = self._get_attribute_by_name(obj1, obj2, number_type)
        code = self._get_code_from_phone(number)

        if code in self.number_of_calls_by_code:
            self.number_of_calls_by_code[code] += 1
        else:
            self.number_of_calls_by_code[code] = 1

    def _increase_summary_duration_by_code(
            self, obj1, obj2, duration, number_type):
        """
        Increases summary duration of calls by specific code in s
        elf.summary_duration_by_code dict.

        :param obj1: <object> Call or Duration.
        :param obj2: <object> Call or Duration.
        :param duration: <int> duration of call (from Duration object).
        :param number_type: <str> source_number or dest_number.
        """

        number = self._get_attribute_by_name(obj1, obj2, number_type)
        code = self._get_code_from_phone(number)

        if code in self.summary_duration_by_code:
            self.summary_duration_by_code[code] += duration
        else:
            self.summary_duration_by_code[code] = duration

    def refresh_stats(self, obj1, obj2):
        """
        Refresh current daily stats (self.self.summary_number_of_calls,
        self.summary_calls_duration, etc) based on obj1 and obj2.

        :param obj1: <object> Call or Duration.
        :param obj2: <object> Call or Duration.
        :return:
        """

        # общее количество звонков
        self.summary_number_of_calls += 1

        # суммарная длительность звонков
        new_duration = self._get_attribute_by_name(obj1, obj2, "duration")
        self.summary_calls_duration += new_duration

        # кол-во звонков по каждому телефонному коду
        self._increase_number_of_calls_by_code(obj1, obj2, "source_number")
        self._increase_number_of_calls_by_code(obj1, obj2, "dest_number")

        # сумарная длительлность по каждому телефонному коду
        self._increase_summary_duration_by_code(
            obj1, obj2, new_duration, "source_number")
        self._increase_summary_duration_by_code(
            obj1, obj2, new_duration, "dest_number")
