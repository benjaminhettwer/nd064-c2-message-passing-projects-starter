from datetime import datetime
import logging
import os
import json

from app.connections.models import Location
from app.connections.schemas import (
    ConnectionSchema,
    LocationSchema,
)
from app.connections.services import ConnectionService, LocationService
from flask import request, g, Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List, Dict

DATE_FORMAT = "%Y-%m-%d"

TOPIC_NAME = os.environ["TOPIC_NAME"]

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa
logger = logging.getLogger("connections-api")


# TODO: This needs better exception handling


#@api.route("/locations")
@api.route("/locations/", methods=['GET', 'POST'])
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    #@api.doc(body=LocationSchema)
    def post(self) -> Location:
        data = request.get_json()
        #location: Location = LocationService.create(request.get_json())
        
        # Turn order_data into a binary string for Kafka
        kafka_data = json.dumps(data).encode()
        
        kafka_producer = g.kafka_producer
        kafka_producer.send(TOPIC_NAME, kafka_data)
        kafka_producer.flush()
        
        return Response(status=202)

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location

@api.route("/connection/<person_id>")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        results = ConnectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )
        return results
