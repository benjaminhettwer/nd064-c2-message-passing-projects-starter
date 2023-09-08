## Docker commands used to setup DB
docker pull postgis/postgis
docker run -d -p 5432:5432 --name postgres-postgis --env-file .env postgres/postgis
docker cp ../../db postgres-postgis:/
docker exec -it postgres-postgis psql -U $POSTGRES_USER -d $POSTGRES_DB -a -f db/2020-08-15_init-db.sql
docker exec -it postgres-postgis psql -U $POSTGRES_USER -d $POSTGRES_DB -a -f db/udaconnect_public_person.sql
docker exec -it postgres-postgis psql -U $POSTGRES_USER -d $POSTGRES_DB -a -f db/udaconnect_public_location.sql


## Docker commands used to build and run the application
docker build -t persons-api .
docker run -d -p 30005:5000 --name persons-api --env-file .env persons-api

## Env variables required to start the application
DB_USERNAME
DB_PASSWORD
DB_HOST
DB_PORT
DB_NAME

## GRPC commands to generate files (executed from inside /grpc_server folder)
python -m grpc_tools.protoc -I ../../protobufs  --python_out=./ --grpc_python_out=./ ../../protobufs/person.proto

## GRPC commands to start server (executed from inside /grpc_server folder)
python3 person_grpc_server.py 