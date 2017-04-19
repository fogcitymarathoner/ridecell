from datetime import datetime as dt
from django.conf.urls import url
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from parkingspot.models import ParkSpot
from parkingspot.models import ParkSpotReservation


class ParkSpotResource(ModelResource):
  class Meta:
    queryset = ParkSpot.objects.all()
    resource_name = 'parkspot'

  def prepend_urls(self):
    return [
      url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
          self.wrap_view('get_search'), name="api_get_search"),
    ]

  def get_search(self, request, **kwargs):
    """http://localhost:8000/api/parkspots/parkspot/search/?format=json"""
    self.method_check(request, allowed=['get'])

    objects = []

    for ps in ParkSpot.objects.all():
      if ps.is_available():
        objects.append(ps)

    object_list = {
      'objects': objects,
    }

    return self.create_response(request, object_list)


class ParkSpotReservationResource(ModelResource):
  class Meta:
    queryset = ParkSpotReservation.objects.all()
    resource_name = 'parkspotreservation'

  def prepend_urls(self):
    return [
      url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
          self.wrap_view('get_search'), name="api_get_search"),
    ]

  def get_search(self, request, **kwargs):
    """http://localhost:8000/api/parkspotreservations/parkspotreservation/search/?format=json&id=1&rstart=1970-01-0100:00&rend=1970-01-00:30"""
    # fixme: make this PATCH
    self.method_check(request, allowed=['get'])
    reservation = ParkSpotReservation(id=request.GET['id'],
                                      rstart=dt.strptime(request.GET['rstart'], '%Y-%m-%s%H%M'),
                                      rend=dt.strptime(request.GET['rend'], '%Y-%m-%s%H%M'))
    reservation.save()
    objects = []

    objects.append(reservation)

    object_list = {
      'objects': objects,
    }

    return self.create_response(request, object_list)
