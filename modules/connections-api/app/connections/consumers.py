import os
import json
import logging
from kafka import KafkaConsumer
from app.connections.services import LocationService


logger = logging.getLogger("connections-api")
logging.basicConfig(level=logging.WARNING)


TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER_URL = os.environ["KAFKA_SERVER_URL"]

consumer = KafkaConsumer(TOPIC_NAME)

def fetch_locations(app_context):
    
    consumer = KafkaConsumer(TOPIC_NAME, group_id='location-group', bootstrap_servers=KAFKA_SERVER_URL)
    
    while True:
        try:
            records = consumer.poll(timeout_ms=1000)

            for _, locations in records.items():
                for loc in locations:
                    location_parsed = json.loads(loc.value)
                    #logger.debug("Received message from broker: " + str(location_parsed))
                    print("Received message from broker: " + str(location_parsed))
                    
                    with app_context:
                        LocationService.create(location_parsed)
            continue
        except Exception as e:
            logger.error(e)
            continue