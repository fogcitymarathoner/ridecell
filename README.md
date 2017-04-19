Parking Spot
============

Python 3.6
uses tastypie as api framework

uses sqlite3 as database

python manage.py migrate # creates database

python manage.py runserver # starts localhost:8000

Endpoints
=========
list available spots
http://localhost:8000/api/parkspots/parkspot/search/?format=json
reserve a spot
http://localhost:8000/api/parkspotreservations/parkspotreservation/search/?format=json&id=1&rstart=1970-01-0100:00&rend=1970-01-00:30