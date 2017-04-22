import sys
from datetime import datetime as dt
import logging

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()

class ParkSpot(Base):
    __tablename__ = 'parkspot'

    id = sa.Column(sa.Integer, primary_key=True)
    lat = sa.Column(sa.Float)
    lng = sa.Column(sa.Float)

    def __repr__(self):
      return "<ParkSpot(id='%s', lat='%s', lng='%s')>" % (
        self.id, self.lat, self.lng)

    def is_available(self, session, rstart=None, rend=None):
      if rstart is None and rend is None:
        rstart = dt.now()
        rend = dt.now()
      try:
        reservations = session.query(Reservation).\
          filter(Reservation.parkspot_id==self.id).\
          filter(Reservation.starttime>=rstart).\
          filter(Reservation.starttime<=rend)
        if reservations.count():
          return False
        else:
          return True
      except NoResultFound:
        return True
      except:
        logging.error('Something bad happened reading the reservations table')
        logging.error("Unexpected error:", sys.exc_info()[0])
        raise

    def to_dict(self):
      return {}
    def reserve(self, session, user, rstart, rend):
      """Reserve a parkspot
      return: reservation if successful, else False
      """

      if self.is_available(session, rstart, rend):
        try:
          res = Reservation(parkspot=self, user=user, starttime=rstart, endtime=rend)
          session.add(res)
          session.commit()
          return res
        except:
          logging.error('Something bad happened saving reservation.')
          logging.error("Unexpected error:", sys.exc_info()[0])
          session.rollback()
          raise
        else:
          session.rollback()
          return False
      else:
        return False


class Reservation(Base):
    __tablename__ = 'reservation'

    id = sa.Column(sa.Integer, primary_key=True)
    parkspot_id = sa.Column(sa.Integer, sa.ForeignKey('parkspot.id'), nullable=False)
    parkspot = relationship("ParkSpot")
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)
    user = relationship("User")
    starttime = sa.Column(sa.DateTime)
    endtime = sa.Column(sa.DateTime)

    def __repr__(self):
      return "<Reservation(id='%s', parkspot.id='%s', user.id='%s', start='%s', end='%s')>" % (
        self.id, self.parkspot_id, self.user_id,
        self.starttime.strftime('%m/%d/%y %H:%M'), self.endtime.strftime('%m/%d/%y %H:%M'))

class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(32))

    def __repr__(self):
      return "<user(id='%s', name='%s')>" % (self.id, self.name)
