import psycopg2
from psycopg2 import sql
from config import Config

def create_database():
    # Parse the database URL
    db_url = Config.SQLALCHEMY_DATABASE_URI
    db_name = db_url.rsplit('/', 1)[-1]

    # Create a connection to the default database to create our target database
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
    conn.autocommit = True

    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    # Check if the database already exists
    cursor.execute(sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"), [db_name])
    exists = cursor.fetchone()

    if not exists:
        # Create the database if it does not exist
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))

    # Close the connection
    cursor.close()
    conn.close()
