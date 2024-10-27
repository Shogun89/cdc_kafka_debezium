import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User
from database import MYSQL_CONNECTION_STRING, POSTGRES_CONNECTION_STRING

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mysql_engine = create_engine(MYSQL_CONNECTION_STRING)
postgres_engine = create_engine(POSTGRES_CONNECTION_STRING)

MySQLSession = sessionmaker(bind=mysql_engine)
PostgresSession = sessionmaker(bind=postgres_engine)


def get_table_data(session, model):
    return session.query(model).all()


def object_to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in obj.__table__.columns}


def compare_values(mysql_val, postgres_val):
    return mysql_val == postgres_val


def compare_databases():
    logger.info("Starting database comparison for users table")

    mysql_session = MySQLSession()
    postgres_session = PostgresSession()

    try:

        mysql_users = get_table_data(mysql_session, User)
        postgres_users = get_table_data(postgres_session, User)

        mysql_count = len(mysql_users)
        postgres_count = len(postgres_users)

        logger.info(f"User count: MySQL ({mysql_count}), PostgreSQL ({postgres_count})")

        if mysql_count != postgres_count:
            logger.warning(
                f"Mismatch in number of users: MySQL ({mysql_count}) vs PostgreSQL ({postgres_count})"
            )

        for mysql_user, postgres_user in zip(mysql_users, postgres_users):
            mysql_dict = object_to_dict(mysql_user)
            postgres_dict = object_to_dict(postgres_user)

            if not all(
                compare_values(mysql_dict[key], postgres_dict[key])
                for key in mysql_dict.keys()
            ):
                logger.warning(f"Mismatch in user records:")
                logger.warning(f"  MySQL: {mysql_dict}")
                logger.warning(f"  PostgreSQL: {postgres_dict}")
                for key in mysql_dict.keys():
                    if not compare_values(mysql_dict[key], postgres_dict[key]):
                        logger.warning(
                            f"    Difference in '{key}': MySQL={mysql_dict[key]}, PostgreSQL={postgres_dict[key]}"
                        )
            else:
                logger.info(f"User {mysql_dict['id']} matches in both databases")

    finally:
        mysql_session.close()
        postgres_session.close()

    logger.info("Database comparison for users table completed")


if __name__ == "__main__":
    compare_databases()
