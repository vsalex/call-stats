from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from app.db_models import Base, DailyStat, CodeStat


class DBManager(object):
    def __init__(self):
        engine = create_engine('sqlite:///daily_stat.sqlite', echo=False)
        # Create session maker
        session = sessionmaker()
        # Bind session to db (engine)
        session.configure(bind=engine)
        # Create all bases if it is necessary
        Base.metadata.create_all(engine)

        # Create session in which we will work
        self.s = session()

    def _update_daily_stat(self, ds_db, ds_queue):
        """
        Refresh all information in DB for current DailyStat.

        :param ds_db: <object> DailyStat from DB.
        :param ds_queue: <object> DailyStat from CallDurationQueue.
        """

        ds_db.summary_number_of_calls = ds_queue.summary_number_of_calls
        ds_db.summary_calls_duration = ds_queue.summary_calls_duration
        ds_db.do_not_matched_calls = ds_queue.do_not_matched_duration
        ds_db.do_not_matched_duration = ds_queue.do_not_matched_duration

        self.s.add(ds_db)

    def _add_daily_stat(self, ds_queue):
        """
        Add new DailyStat to DB.

        :param ds_queue: <object> DailyStat from CallDurationQueue.
        """

        new_db_ds = DailyStat(
            date=ds_queue.current_date,
            summary_number_of_calls=ds_queue.summary_number_of_calls,
            summary_calls_duration=ds_queue.summary_calls_duration,
            do_not_matched_calls=ds_queue.do_not_matched_calls,
            do_not_matched_duration=ds_queue.do_not_matched_duration,
        )

        self.s.add(new_db_ds)

        return new_db_ds

    def _update_related_codes(self, ds_db, ds_queue_codes_stat):
        """
        Refresh all related codes for current daily stat.

        :param ds_db: <object> DailyStat from DB.
        :param ds_queue_codes_stat: <dict> of convenient code stats
        representation for DB.
        """

        # This case can be if on some day we got only one outdated duration
        # json input
        if not ds_queue_codes_stat:
            return None

        # Update current codes
        for code_db in ds_db.codes:
            cur_code_from_db = code_db.phone_code

            # Pop code data from ds_code_stat
            cur_code_data = ds_queue_codes_stat.pop(cur_code_from_db)

            code_db.number_of_calls = cur_code_data["number_of_calls"]
            code_db.summary_duration = cur_code_data["summary_duration"]

            self.s.add(code_db)

        # If there are some new codes
        for code, data in ds_queue_codes_stat.items():
            new_code = CodeStat(
                phone_code=code,
                number_of_calls=data["number_of_calls"],
                summary_duration=data["summary_duration"],
                daily_stat=ds_db,
            )
            self.s.add(new_code)

    @staticmethod
    def _get_all_code_statistic_for_day(daily_stat):
        """
        Get full statistics by concrete phone code by DailyStat from
        CallDurationQueue. It just creates more convenient data structure for
        DB,

        :param daily_stat: <object> DailyStat from CallDurationQueue.
        :return: <dict> of convenient code stats representation for DB.
        """

        # This case can be if on some day we got only one outdated duration
        # json input
        if not daily_stat:
            return None

        daily_stat_codes = {}
        for code, num in daily_stat.number_of_calls_by_code.items():
            # Create inherit dictionaries
            daily_stat_codes.update({code: {
                "number_of_calls": num
            }})

        for code, dur in daily_stat.summary_duration_by_code.items():
            # Update inherit dictionaries
            daily_stat_codes[code].update({
                "summary_duration": dur
            })

        return daily_stat_codes

    def write_data_to_db(self, full_stat):
        """
        Write all data from FullStat object to DB.

        :param full_stat: <object> FullStat with all DailyStat's from
        CallDurationQueue,
        """

        for daily_stat in full_stat.daily_stats:

            # Try to find this daily stat in DB
            try:
                query_result = self.s.query(DailyStat).filter(
                    DailyStat.date == daily_stat.current_date).one()
            except NoResultFound:
                query_result = None

            daily_stat_codes = self._get_all_code_statistic_for_day(daily_stat)

            # If we found this daily stat in DB
            if query_result:
                self._update_daily_stat(query_result, daily_stat)
                self._update_related_codes(query_result, daily_stat_codes)
            # If there is no this day in DB
            else:
                new_ds_db = self._add_daily_stat(daily_stat)
                self._update_related_codes(new_ds_db, daily_stat_codes)

            self.s.commit()
