from datetime import datetime

from app.dailystat import DailyStat


class FullStat(object):
    """
    Contain daily stats for every day. It can add new DailyStat or refresh some
    statistics on existing.

    In production i shall add here some methods that clear outdated daily stats
    from here, but it depend on real case.
    """

    def __init__(self):
        self.daily_stats = []

    def _get_daily_stat_for_call(self, call_obj):
        """
        Return DailyStat object the day when concrete call was made.

        :param call_obj: <object> Call.
        :return: <object> DailyStat.
        """

        for elem in self.daily_stats:
            if elem.current_date == call_obj.timestamp.date():
                return elem

    def _get_today_daily_stat(self):
        """
        Get today DailyStat object.

        :return: <object> DailyStat.
        """
        for elem in self.daily_stats:
            if elem.current_date == datetime.now().date():
                return elem

    def _add_matched_to_daily_stats(self, matched):
        """
        Add new DailyStat to self.daily_stats or refresh existing DailyStat.

        :param matched: <dict> with Call and Duration objects.
        """

        cur_daily_stat = self._get_daily_stat_for_call(matched["call"])

        # If we didn't find daily stat with date same as in current call then
        # append new DailyStat object
        if not cur_daily_stat:
            new_daily_stat = DailyStat(
                current_date=matched["call"].timestamp.date())
            self.daily_stats.append(new_daily_stat)
            cur_daily_stat = self.daily_stats[-1]

        cur_daily_stat.refresh_stats(matched["call"], matched["duration"])

    def make_action(self, queue_result):
        """
        Make actions depend on whats coming in queue_result. If we got some
        unkown actions then NameError will be raised

        :param queue_result: <dict> with CallDurationQueue.add_object() method.
        """

        # If there are no queue result coming, then do nothing
        if not queue_result:
            return

        if "matched" in queue_result:
            self._add_matched_to_daily_stats(queue_result["matched"])
            del queue_result["matched"]

        if "outdated_calls" in queue_result:
            self._remove_outdated_calls(queue_result["outdated_calls"])
            del queue_result["outdated_calls"]

        if "outdated_durations" in queue_result:
            self._remove_outdated_duration(queue_result["outdated_durations"])
            del queue_result["outdated_durations"]

        if queue_result:
            raise NameError("Got some unknown actions %s in queue result!" %
                            queue_result)

    def _remove_outdated_calls(self, outdated_calls):
        """
        Increase do_not_matched_calls counter for every outdated call
        from queue.

        :param outdated_calls: <list> of outdated calls.
        """

        for outdated_call in outdated_calls:
            cur_daily_stat = self._get_daily_stat_for_call(outdated_call)
            cur_daily_stat.do_not_matched_calls_number += 1

    def _remove_outdated_duration(self, outdated_durations):
        """
        Increase do_not_matched_duration counter for every outdated
        duration from queue. Because we don't know to which daily stat current
        duration belongs (duration have not timestamp field) than increase
        do_not_matched_duration counter for today daily_stat.

        Here can be some analysis by call_id to determinate approximately day
        but i'm not sure about necessity of this action.

        :param outdated_durations: <list> of outdated durations.
        """

        for outdated_duration in outdated_durations:
            cur_daily_stat = self._get_today_daily_stat()

            # If there is no today daily stat, then create it
            if not cur_daily_stat:
                cur_daily_stat = DailyStat(current_date=datetime.now().date())
                self.daily_stats.append(cur_daily_stat)

            cur_daily_stat.do_not_matched_duration += 1
