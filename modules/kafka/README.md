## Docker commands to start kafka container
docker-compose up -d

# Command to create topic (execute inside local kafka installation)
bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9094

# Command to write into topic (execute inside local kafka installation)
bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:9094

# Command to read events from topic (execute inside local kafka installation)
bin/kafka-console-consumer.sh --topic quickstart-events --from-beginning --bootstrap-server localhost:9094
