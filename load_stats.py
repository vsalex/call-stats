from app.loader import Loader
from app.call_duration_queue import CallDurationQueue
from app.full_stat import FullStat
from app.db_manager import DBManager


if __name__ == '__main__':
    # ЗАГЛУШКАЗАГЛУШКАЗАГЛУШКАЗАГЛУШКАЗАГЛУШКАЗАГЛУШКАЗАГЛУШКАЗАГЛУШКА
    l = Loader()
    all_files = l.load()

    # Initialize queue object for in memory queue for calls and duration.
    queue = CallDurationQueue()

    # Initialize full_stat object which contains from daily_stats object. I
    # decide to use it because i can have call objects for several days and
    # thus i must have several daily_stat's objects.
    full_stat = FullStat()

    # This object manage writing data to DB.
    db_manager = DBManager()

    for _obj in all_files:
        queue_result = queue.add_object(_obj)
        full_stat.make_action(queue_result)
        db_manager.write_data_to_db(full_stat)

    for daily_stat in full_stat.daily_stats:
        print(daily_stat.__dict__)
