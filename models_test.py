from datetime import datetime as dt
from datetime import timedelta as td
import pytz
import random
import string
import unittest

from flask import Flask
from flask_testing import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import ParkSpot
from models import Reservation
from models import User

import testing


class ParkSpotModelTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config.from_object('config_test')
        return app

    def setUp(self):
      super(ParkSpotModelTest, self).setUp()
      app = self.create_app()
      engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
      sessionMaker = sessionmaker(bind=engine)
      self.session = sessionMaker()
      self.parkingspots = []
      self.users = []
      for i in range(5):
        ps = ParkSpot(
          lat=random.uniform(1.0, 64.0),
          lng=random.uniform(1.0, 64.0),
        )
        self.session.add(ps)
        self.session.commit()
        self.parkingspots.append(ps)
        ps.is_available(self.session)

      for i in range(5):
        u = User(name=testing.random_string(5))
        self.session.add(u)
        self.session.commit()
        self.users.append(u)
      self.session.commit()

    def tearDown(self):
      for o in self.session.query(ParkSpot).all() + \
            self.session.query(Reservation).all() + \
            self.session.query(User).all():
        self.session.delete(o)
      self.session.commit()

    def test_new_parkspots_available(self):
      """Tests that newly minted parkspots are available"""
      for ps in self.parkingspots:
        self.assertTrue(ps.is_available(self.session))

    def test_parkspot_reservation(self):
      """Tests parkspot unavailable after reservation"""
      rstart = testing.epoch
      rend = testing.epoch + td(hours=1)
      self.parkingspots[0].reserve(self.session, self.users[0], rstart=rstart, rend=rend)
      self.assertFalse(self.parkingspots[0].is_available(self.session, rstart=rstart, rend=rend))

if __name__ == '__main__':
    unittest.main()
