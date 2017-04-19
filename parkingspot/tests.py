from datetime import datetime as dt
from datetime import timedelta as td
import pytz
import random
import string

from django.contrib.auth.models import User
from django.test import TestCase

from parkingspot.models import ParkSpot
from parkingspot.models import ParkSpotReservation


epoch = dt(year=1970, month=1, day=1, hour=0, minute=0, tzinfo=pytz.UTC)

def random_string(N):
  return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

class ParkSpotModelTest(TestCase):

    def setUp(self):
      self.parkingspots = []
      self.users = []
      for i in range(5):
        ps = ParkSpot(
          lat=random.uniform(1.0, 64.0),
          lng=random.uniform(1.0, 64.0),
          radius=random.uniform(1.0, 64.0))
        ps.save()
        self.parkingspots.append(ps)
      for i in range(5):
        u = User(
          username=random_string(5),
          email = '%s.%s.com' % (random_string(5), random_string(5))
        )
        u.save()
        self.users.append(u)

    def tearDown(self):
      ParkSpot.objects.all().delete()

    def test_parkingspot_insert(self):
        """
        test parking spot table is writable
        """
        self.assertEqual(5, len(ParkSpot.objects.all()))

    def test_parkingspot_reservation(self):
        """
        test that parking spots reservable
        """
        self.parkingspots[0].reserve(self.users[0], epoch, epoch+td(hours=1))



    def test_parkingspot_is_available(self):
        """
        test parking spot table is writable
        """
        self.parkingspots[0].reserve(self.users[0], epoch, epoch+td(hours=1))
        self.assertFalse(self.parkingspots[0].is_available(epoch, epoch+td(hours=1)))


