# Change Data Capture (CDC) with Debezium, Kafka, MySQL, FastAPI and PostgreSQL

## Setup

1. Install Docker and Docker Compose.
2. Clone this repository.
3. Run `docker-compose up --build -d` to start all services.
4. Wait for a few minutes to allow all services to start up properly.
5. Check the logs of the app to ensure it is running correctly.

## Usage

The application should now be running with MySQL as the primary database, Kafka and Debezium for CDC, and PostgreSQL as the target database for replication.

Any changes made to the MySQL database through the FastAPI application will be automatically captured by Debezium, sent to Kafka, and then inserted into PostgreSQL.

To test the setup, you can use the FastAPI endpoints to create, read, update, or delete data, and then check both the MySQL and PostgreSQL databases to verify that the changes are being replicated correctly.

## Testing Checklist
This is a checklist to test the setup. It is not entirely necessary to test all of these points, but it is a good way to verify that the setup is working correctly.

1. Test Kafka and Debezium setup:
   - [ ] Verify Kafka is running correctly in Docker
   - [ ] Check if Debezium connector is properly configured
   - [ ] Ensure Debezium is capturing changes from MySQL

2. Test PostgreSQL replication:
   - [ ] Verify data is being replicated from MySQL to PostgreSQL

3. API Endpoint Testing:
   - [ ] Test all CRUD operations for Users
   - [ ] Test all CRUD operations for Products
   - [ ] Test all CRUD operations for Orders
   - [ ] Test all CRUD operations for OrderItems

4. Database Consistency Check:
   - [ ] Compare data in MySQL and PostgreSQL after running `generate_test_data.py`
   - [ ] Manually create, update, and delete records and check both databases

5. Error Handling and Edge Cases:
   - [ ] Test API with invalid data
   - [ ] Test system behavior when Kafka or PostgreSQL is down

6. Logging and Monitoring:
   - [ ] Verify all components are logging correctly
   - [ ] Set up monitoring for Kafka, Debezium, and PostgreSQL

7. Documentation:
   - [ ] Update README with any new setup steps or requirements
   - [ ] Document any known issues or limitations

8. Clean-up and Reset:
   - [ ] Create scripts to reset the databases for fresh testing

9. Integration Testing:
    - [ ] Test the entire flow from data creation to replication

## Ensuring Debezium is Capturing Changes

To verify that Debezium is correctly capturing changes from MySQL and sending them to Kafka:

1. Ensure your Docker environment is up and running:   
```
   docker-compose up -d   
```

2. Register the Debezium connector:   
```
   curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/ -d @mysql-source.json
``` 
You should see a response like this:
```
HTTP/1.1 201 Created
Date: Sat, 26 Oct 2024 20:10:49 GMT
Location: http://localhost:8083/connectors/mysql-connector
Content-Type: application/json
Content-Length: 532
Server: Jetty(9.4.44.v20210927)

{"name":"mysql-connector","config":{"connector.class":"io.debezium.connector.mysql.MySqlConnector","tasks.max":"1","database.hostname":"mysql","database.port":"3306","database.user":"root","database.password":"rootpassword","database.server.id":"184054","database.server.name":"mysql","database.include.list":"fastapi_db","database.history.kafka.bootstrap.servers":"kafka:9092","database.history.kafka.topic":"schema-changes.fastapi_db","database.allowPublicKeyRetrieval":"true","name":"mysql-connector"},"tasks":[],"type":"source"}
```
3. Check if the connector was created successfully:   
```
   curl -H "Accept:application/json" localhost:8083/connectors/
```
You should see a response like this:
```
[mysql-connector]
```
4. Check the status of the connector (should be RUNNING):   
```   
   curl -H "Accept:application/json" localhost:8083/connectors/mysql-connector/status
```
You should see a response like this:
```
{"name":"mysql-connector","connector":{"state":"RUNNING","worker_id":"172.18.0.7:8083"},"tasks":[{"id":0,"state":"RUNNING","worker_id":"172.18.0.7:8083"}],"type":"source"}
```

5. Insert test data into MySQL:   
```
   docker-compose exec mysql mysql -uroot -prootpassword fastapi_db -e "INSERT INTO users (email, is_active) VALUES ('test@example.com', TRUE);"   
```
You should see a response like this:
```
mysql: [Warning] Using a password on the command line interface can be insecure.
```
6. Verify the data was inserted correctly:   
```
   docker-compose exec mysql mysql -uroot -prootpassword fastapi_db -e "SELECT * FROM users;"   
```
You should see a response like this:
```
mysql: [Warning] Using a password on the command line interface can be insecure.
+----+------------------+-----------+------------+------------+
| id | email            | is_active | created_at | last_login |
+----+------------------+-----------+------------+------------+
|  1 | test@example.com |         1 | NULL       | NULL       |
+----+------------------+-----------+------------+------------+
```

7. List Kafka topics to ensure the MySQL topics are created:   
```
   docker-compose exec kafka /kafka/bin/kafka-topics.sh --list --bootstrap-server kafka:9092   
```
You should see a response like this:
```
__consumer_offsets
my_connect_configs
my_connect_offsets
my_connect_statuses
mysql
mysql.fastapi_db.users
schema-changes.fastapi_db
```
8. Check the topics created by Debezium:
```
   curl -H "Accept:application/json" localhost:8083/connectors/mysql-connector/topics
```
You should see a response like this:
```
{"mysql-connector":{"topics":["mysql","mysql.fastapi_db.users"]}}
```
9. Consume messages from the Kafka topic:  
```
   docker-compose exec kafka /kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic mysql.fastapi_db.users --from-beginning --max-messages 1   
```   

You should see a payload like this

```
"payload": {
    "before": null,
    "after": {
      "id": 1,
      "email": "test@example.com",
      "is_active": 1,
      "created_at": null,
      "last_login": null
    },
```

## Verifying data is being replicated from MySQL to PostgreSQL

1. Run Docker Compose: ```
   docker-compose up -d```
2. Create a test user: ```
   docker-compose exec mysql mysql -uroot -prootpassword fastapi_db -e "INSERT INTO users (email, is_active) VALUES ('test@example.com', TRUE);"  ```
3. Check the PostgreSQL database to verify that the data has been replicated correctly: ```
   docker-compose exec postgres psql -U postgres -d fastapi_db -c "SELECT * FROM users;" ```

You should see a response like this:
```
 id |      email       | is_active |         created_at         | last_login 
----+------------------+-----------+----------------------------+------------
  1 | test@example.com | t         | 2024-10-26 21:43:54.992539 |
(1 row)
```
