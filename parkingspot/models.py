from datetime import datetime as dt

from django.db import models
from django.contrib.auth.models import User


class ParkSpot(models.Model):
  lat = models.FloatField(null=True, blank=True)
  lng = models.FloatField(null=True, blank=True)
  radius = models.FloatField(null=True, blank=True)

  def is_available(self, rstart=None, rend=None):
    if rstart is None and rend is None:
      rstart = dt.now()
      rend = dt.now()
    try:
      reservations = ParkSpotReservation.objects. \
        filter(id=self.id). \
        filter(starttime__gte=rstart). \
        filter(endtime__lte=rend)
      if len(reservations) > 0:
        return False
      else:
        return True
    except:
      print('Something bad happened reading the reservations table')

  def reserve(self, user, rstart, rend):
    """Returns reservation if successful
    else False"""
    reservation = ParkSpotReservation(parkspot=self, user=user, starttime=rstart, endtime=rend)
    if self.is_available(rstart, rend):
      try:
        reservation.save()
        return reservation
      except:
        print('Something bad happened saving reservation.')
        raise
    else:
      return False


class ParkSpotReservation(models.Model):
  user = models.OneToOneField(User)
  parkspot = models.ForeignKey(ParkSpot)
  starttime = models.DateTimeField()
  endtime = models.DateTimeField()