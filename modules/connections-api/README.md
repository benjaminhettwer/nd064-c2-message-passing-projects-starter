## Docker commands used to setup DB
docker pull postgis/postgis
docker run -d -p 5432:5432 --name postgres-postgis --env-file .env postgres/postgis
docker cp ../../db postgres-postgis:/
docker exec -it postgres-postgis psql -U $POSTGRES_USER -d $POSTGRES_DB -a -f db/2020-08-15_init-db.sql
docker exec -it postgres-postgis psql -U $POSTGRES_USER -d $POSTGRES_DB -a -f db/udaconnect_public_person.sql
docker exec -it postgres-postgis psql -U $POSTGRES_USER -d $POSTGRES_DB -a -f db/udaconnect_public_location.sql


## Docker commands used to build and run the application
docker build -t connections-api .
docker run -d -p 30007:5000 --name connections-api --env-file .env connections-api

## Env variables required to start the application (Kafka container has to be running)
DB_USERNAME
DB_PASSWORD
DB_HOST
DB_PORT
DB_NAME
PERSONS_SERVICE_HOST
PERSONS_SERVICE_PORT
KAFKA_SERVER_URL
TOPIC_NAME


## GRPC commands (executed from inside /grpc_client folder)
python -m grpc_tools.protoc -I ../../../../protobufs/  --python_out=./ --grpc_python_out=./ ../../../../protobufs/person.proto
# Modify import statement in person_pb2_grpc.py: 'import person_pb2 as person__pb2' => 'from . import person_pb2 as person__pb2 (see https://github.com/protocolbuffers/protobuf/issues/1491 )