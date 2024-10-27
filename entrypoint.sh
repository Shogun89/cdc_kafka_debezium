#!/bin/sh

echo "Starting entrypoint script..."

echo "Waiting for MySQL..."
while ! nc -z mysql 3306; do
  sleep 1
done
echo "MySQL is up"

echo "Running database initialization..."
python /app/fastapi/init_db.py

echo "Waiting for Kafka and Debezium..."
sleep 30

echo "Registering Debezium connector..."
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://connect:8083/connectors/ -d @/app/mysql-source.json


echo "Waiting for Debezium connector to be ready..."
until curl -s -f -o /dev/null http://connect:8083/connectors/mysql-connector/status; do
    echo "Debezium connector not ready, waiting..."
    sleep 5
done
echo "Debezium connector is ready"

echo "Listing Kafka topics..."
docker-compose exec kafka kafka-topics.sh --list --bootstrap-server kafka:9092

echo "Starting Kafka to Postgres consumer in the background..."
python /app/fastapi/kafka_to_postgres.py &

echo "Changing directory to /app/fastapi..."
cd /app/fastapi

echo "Starting the FastAPI server in the background..."
uvicorn main:app --host 0.0.0.0 --port 8000 &

echo "Waiting for FastAPI server to start..."
sleep 30

echo "Generating test data..."
python /app/fastapi/generate_test_data.py

# After starting the Kafka to Postgres consumer
echo "Waiting for data to propagate..."
sleep 30

# Then run the comparison
echo "Comparing databases (users only)..."
python /app/fastapi/compare_databases.py

echo "Entrypoint script completed. Keeping container running..."
tail -f /dev/null
