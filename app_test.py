import mock
import unittest

from app import app
from models import ParkSpot
from models import Reservation
from models import User


class ParkSpotApiTest(unittest.TestCase):

    def setUp(self):
      super(ParkSpotApiTest, self).setUp()
      self.client = app.test_client()

    def tearDown(self):
      for o in self.session.query(ParkSpot).all() + \
            self.session.query(Reservation).all() + \
            self.session.query(User).all():
        self.session.delete(o)
      self.session.commit()

    @mock.patch('models.ParkSpot')
    def test_post_parkspot(self, mockUser):
      """Tests posting new parkspots"""
      with app.test_client() as c:
        c.post('/',
            data={
              'lat': 0.1,
              'lng': 2.3
        })
        mockUser.assert_called_with(lat=0.1, lng=2.3)

if __name__ == '__main__':
    unittest.main()
