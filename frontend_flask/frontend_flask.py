import re
from datetime import datetime, timedelta

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import and_

import config

# Some ugly hacks with paths (define in config.py). I can't invent something
# more likely :(.
from app import utils

app = Flask(__name__, template_folder='templates')
app.config.from_object(config)

db = SQLAlchemy(app)
db.init_app(app)


def _get_code_statistics(code_from_url, weekly_db_stat, kwargs):
    """Count's some phone codes statistics define on weekly_db_stat."""

    # Check phone code from url format
    result = re.search(utils.code_number_format, code_from_url)
    if not result:
        kwargs.update({"code_error": "Wrong phone code url format! It must be "
                                     "something like: "
                                     "?phone_code=%2B7+(901)"})
        return kwargs

    phone_codes_stat = {
        "number_of_calls": 0,
        "summary_duration": 0,
    }

    for daily_stat in weekly_db_stat:
        for elem in daily_stat.codes:
            if not elem.phone_code == code_from_url:
                continue

            for stat in phone_codes_stat:
                phone_codes_stat[stat] += getattr(elem, stat)

    kwargs.update({
        "phone_code": code_from_url,
        "phone_codes_stat": phone_codes_stat,
    })

    return kwargs


@app.route("/", methods=['GET'])
def index():
    today = datetime.now().date()

    # !TODO: remove in production
    # Test case for starting fixtures
    today = datetime.strptime('2015 12 31', '%Y %m %d')

    plus_7d = today + timedelta(days=7)
    minus_7d = today - timedelta(days=7)

    # Get weekly stat from DB
    weekly_db_stat = DailyStat.query.filter(
        and_(DailyStat.date >= minus_7d, DailyStat.date <= plus_7d)).all()

    # I think about aggregation of weekly stat, but in this case i will have
    # separate query for all necessary stats, that is worse that collecting
    # weekly stats by hands. In case of ORM aggregation it could look like this
    # db.session.query(DailyStat,
    #                  func.sum(DailyStat.summary_calls_duration).label(
    #                      'calls_duration_by_week')).first()

    clear_weekly_stat = {
        "summary_number_of_calls": 0,
        "summary_calls_duration": 0,
        "do_not_matched_calls": 0,
        "do_not_matched_duration": 0,
    }

    # Fill clear weekly stat
    for day_stat in weekly_db_stat:
        for stat in clear_weekly_stat:
            clear_weekly_stat[stat] += getattr(day_stat, stat)

    # Lets make our stats look clearly (remove underscores)
    for stat in clear_weekly_stat:
        clear_text_stat = stat.replace('_', ' ')
        clear_weekly_stat[clear_text_stat] = clear_weekly_stat.pop(stat)

    kwargs = {
        "week_start": minus_7d,
        "week_end": plus_7d,
        "weekly_stat": clear_weekly_stat,
    }

    # Generate statistics by phone codes
    code_from_url = request.args.get('phone_code')

    if code_from_url:
        kwargs = _get_code_statistics(code_from_url, weekly_db_stat, kwargs)

    return render_template('index.html', **kwargs)

if __name__ == "__main__":
    from models import DailyStat, CodeStat
    app.run()
