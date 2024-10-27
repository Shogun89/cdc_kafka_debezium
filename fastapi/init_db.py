import time
from sqlalchemy.exc import OperationalError
from database import Base, mysql_engine, postgres_engine
from models import *  

def wait_for_db(engine, max_retries=5, retry_interval=5):
    """
    Attempt to connect to a database engine with retries.

    This function tries to establish a connection to the specified database engine.
    If the connection fails, it will retry for a specified number of times with
    a delay between each attempt.

    Args:
        engine: The SQLAlchemy engine to connect to.
        max_retries (int): The maximum number of connection attempts. Defaults to 5.
        retry_interval (int): The time in seconds to wait between retries. Defaults to 5.

    Raises:
        OperationalError: If unable to connect after all retries are exhausted.

    Returns:
        None
    """
    for attempt in range(max_retries):
        try:
            with engine.connect() as connection:
                print(f"Successfully connected to {engine.url}")
                return
        except OperationalError as e:
            if attempt + 1 == max_retries:
                raise
            print(f"Database connection attempt {attempt + 1} failed: {e}")
            time.sleep(retry_interval)

def main():
    print("Waiting for MySQL...")
    wait_for_db(mysql_engine)
    print("Waiting for PostgreSQL...")
    wait_for_db(postgres_engine)
    
    Base.metadata.create_all(bind=mysql_engine)
    Base.metadata.create_all(bind=postgres_engine)
    print("Databases initialized")

if __name__ == "__main__":
    main()
