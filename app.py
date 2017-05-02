import json
import logging
import sys

from flask import request
from flask_alembic import Alembic
from flask_api import FlaskAPI, status, exceptions
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.exceptions import MethodNotAllowed

import models

app = FlaskAPI(__name__)

app.config.from_object('config')

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
sessionMaker = sessionmaker(bind=engine)
session = sessionMaker()

db = SQLAlchemy(app)
alembic = Alembic()
alembic.init_app(app)


@app.route("/", methods=['GET', 'POST'])
def parkspot_list():
    """
    List or create parkspots.
    """
    if request.method == 'POST':
        try:
            lat = request.form.get('lat', default=None, type=float)
            lng = request.form.get('lng', default=None, type=float)
        except ValueError:
            raise MethodNotAllowed
        if lat and lng:
            try:
                parkspot = models.ParkSpot(lat=lat, lng=lng)
                session.add(parkspot)
                session.commit()
                return json.dumps(parkspot.to_dict())
            except:
                logging.error('Something bad happened saving parkspot.')
                logging.error("Unexpected error:", sys.exc_info()[0])
                session.rollback()
                raise

    # request.method == 'GET'
    try:
        lat = request.args.get('lat', default=None, type=float)
        lng = request.args.get('lng', default=None, type=float)
        radius = request.args.get('radius', default=None, type=int) # meters
    except ValueError:
        raise MethodNotAllowed
    if lat and lng and radius:
        # https://johanndutoit.net/searching-in-a-radius-using-postgres/
        q = "SELECT parkspot.id, parkspot.lat, parkspot.lng FROM parkspot WHERE earth_box( ll_to_earth(cast(%s as float8), cast(%s as float8)), %s) @> ll_to_earth(cast(parkspot.lat as float8), cast(parkspot.lng as float8));" % (lat, lng, radius)

        session.execute(q)
        return [json.dumps(ps.to_dict()) for ps in session.execute(q).all()]
    else:
        raise MethodNotAllowed

@app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def parkspot_detail(key):
    """
    Retrieve, update or delete parkspot instances.
    """
    if request.method == 'PUT':
        note = str(request.data.get('text', ''))
        notes[key] = note
        return note_repr(key)

    elif request.method == 'DELETE':
        notes.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in notes:
        raise exceptions.NotFound()
    return note_repr(key)


if __name__ == "__main__":
    app.run(debug=True)