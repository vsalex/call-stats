from sqlalchemy import(
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class DailyStat(Base):
    __tablename__ = 'daily_stat'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    # * общее количество звонков
    summary_number_of_calls = Column(Integer)
    # * суммарная длительность звонков
    summary_calls_duration = Column(Integer)
    # * кол-во несматченных сообщений из очереди Call
    do_not_matched_calls = Column(Integer)
    # * кол-во несматченных сообщений из очереди Duration
    do_not_matched_duration = Column(Integer)

    def __repr__(self):
        return "{0}. on {1} was {2} | {3} | {4} | {5}".format(
            self.id, self.date, self.summary_number_of_calls,
            self.summary_calls_duration, self.do_not_matched_calls,
            self.do_not_matched_duration)


class CodeStat(Base):
    __tablename__ = 'code_stat'

    id = Column(Integer, primary_key=True)
    phone_code = Column(String)
    # * кол-во звонков по каждому телефонному коду
    number_of_calls = Column(Integer)
    # * сумарная длительлность по каждому телефонному коду
    summary_duration = Column(Integer)

    daily_stat_id = Column(Integer, ForeignKey('daily_stat.id'))
    daily_stat = relationship(DailyStat,
                              backref=backref(
                                  'codes',
                                  uselist=True,
                                  cascade='delete,all'))

    def __repr__(self):
        if self.daily_stat_id:
            return "{0}. on {1} is {2} | {3} to {4}".format(
                self.id, self.phone_code, self.number_of_calls,
                self.summary_duration, self.daily_stat_id)
        else:
            return "{0}. on {1} is {2} | {3}".format(
                self.id, self.phone_code, self.number_of_calls,
                self.summary_duration)
