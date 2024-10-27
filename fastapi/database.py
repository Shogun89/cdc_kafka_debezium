from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

MYSQL_CONNECTION_STRING = "mysql://root:rootpassword@mysql:3306/fastapi_db"
POSTGRES_CONNECTION_STRING = "postgresql://postgres:postgrespassword@postgres:5432/fastapi_db"

mysql_engine = create_engine(MYSQL_CONNECTION_STRING)
postgres_engine = create_engine(POSTGRES_CONNECTION_STRING)

MySQLSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)
PostgresSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=postgres_engine)

Base = declarative_base()

def get_mysql_db():
    db = MySQLSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_postgres_db():
    db = PostgresSessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["MySQLSessionLocal", "PostgresSessionLocal", "mysql_engine", "postgres_engine", "Base", "MYSQL_CONNECTION_STRING", "POSTGRES_CONNECTION_STRING", "get_mysql_db", "get_postgres_db", "get_db"]
