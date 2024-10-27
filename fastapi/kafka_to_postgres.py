from kafka import KafkaConsumer
import json
from database import get_postgres_db
import logging
from message_processors import processors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = ['kafka:9092']
KAFKA_TOPICS = [
    'mysql.fastapi_db.users', 
    'mysql.fastapi_db.products', 
    'mysql.fastapi_db.orders', 
    'mysql.fastapi_db.order_items',
    'mysql.fastapi_db.product_categories'
]

def process_message(message):
    """
    Process a Kafka message containing database change events.

    This function parses the message, extracts relevant information,
    and applies the corresponding database operation to PostgreSQL.

    Args:
        message (KafkaMessage): The Kafka message to process.

    Returns:
        None

    Raises:
        KeyError: If the message structure is invalid.
        Exception: For any other processing errors.
    """
    try:
        data = json.loads(message.value)
        logger.info(f"Parsed JSON data: {json.dumps(data, indent=2)}")

        payload = data['payload']
        table = payload['source']['table']
        operation = payload['op']

        if table not in processors:
            logger.warning(f"No processor found for table: {table}")
            return

        db = next(get_postgres_db())
        try:
            if operation in ('c', 'u'):
                processors[table](db, operation, payload['after'])
            elif operation == 'd':
                processors[table](db, operation, payload['before'])
            
            db.commit()
            logger.info(f"Processed {operation} operation for table {table}")
        except Exception as e:
            logger.error(f"Error processing {operation} for table {table}: {e}")
            db.rollback()
        finally:
            db.close()

    except KeyError as e:
        logger.error(f"KeyError processing message: {e}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

def main():
    consumer = KafkaConsumer(
        *KAFKA_TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: x.decode('utf-8')
    )

    logger.info("Starting Kafka to PostgreSQL consumer...")
    for message in consumer:
        process_message(message)

if __name__ == "__main__":
    main()
