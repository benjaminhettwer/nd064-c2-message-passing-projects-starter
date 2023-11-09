#!/bin/sh

# Start the first process
flask run --host 0.0.0.0 &

# Start the second process
python3 grpc_server/person_grpc_server.py &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?