from frontend_flask import db


# I'm not sure about this models, because it is not DRY - i have this
# definition in main app, and this is almost full repeat it. But i'm not sure
# about way i can do not repeat it. In real case i would really think about
# it, because it' look like clumsily now but i don't have clear way to resolve
# it.

class DailyStat(db.Model):
    __tablename__ = 'daily_stat'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    # * общее количество звонков
    summary_number_of_calls = db.Column(db.Integer)
    # * суммарная длительность звонков
    summary_calls_duration = db.Column(db.Integer)
    # * кол-во несматченных сообщений из очереди Call
    do_not_matched_calls = db.Column(db.Integer)
    # * кол-во несматченных сообщений из очереди Duration
    do_not_matched_duration = db.Column(db.Integer)


class CodeStat(db.Model):
    __tablename__ = 'code_stat'

    id = db.Column(db.Integer, primary_key=True)
    phone_code = db.Column(db.String)
    # * кол-во звонков по каждому телефонному коду
    number_of_calls = db.Column(db.Integer)
    # * сумарная длительлность по каждому телефонному коду
    summary_duration = db.Column(db.Integer)

    daily_stat_id = db.Column(db.Integer, db.ForeignKey('daily_stat.id'))
    daily_stat = db.relationship(DailyStat,
                                 backref=db.backref(
                                     'codes',
                                     uselist=True,
                                     cascade='delete,all'))
