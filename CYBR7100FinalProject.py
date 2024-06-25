import sys
import os
import logging
import psycopg2
from psycopg2 import sql
from getpass import getpass

logging.basicConfig(filename="C:/Users/Saiyen Shaw/PycharmProjects/pythonProject/Logging/LOG2",
                    format='%(asctime)s %(message)s',
                    filemode='w')


# Start logging & Threshold
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info("Before connecting to the database")

# Your database connection setup
host = input("Your hosting Information: ")
database = input("Your Database: ")
user = input("Enter Username: ")
password = getpass("Enter Database Password: ")
port = input("Enter Port Number: ")

logger.info("After connecting to the database")

# Log database connection information
logger.info(f"Connecting to database - Host: {host}, Database: {database}, User: {user}, Port: {port}")


connection = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=port
)
connection.set_session(autocommit=True)

with connection.cursor() as cursor:
    cursor.execute('SELECT COUNT(*) FROM users')
    result = cursor.fetchone()
    print(result)


def check_user_for_admin():
    username = input("Let's check if you are admin, Enter your username: ")
    sys.stdout.flush()
    is_admin_result = is_admin(username)
    if is_admin_result:
        print(f"{username} is an admin.")
    else:
        print(f"{username} you are not admin.")


def is_admin(username: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute("""
             SELECT
                 admin
             FROM
                 users
             WHERE
                 username = %(username)s
         """, {
            'username': username
        })
        result = cursor.fetchone()

    if result is None:
        return False
    else:
        admin, = result
        return admin


def count_rows(table_name: str, limit: int) -> int:
    try:
        with connection.cursor() as cursor:
            stmt = sql.SQL("""
                SELECT
                    COUNT(*)
                FROM (
                    SELECT
                        1
                    FROM
                        {table_name}
                    LIMIT
                        {limit}
                ) AS limit_query
            """).format(
                table_name=sql.Identifier(table_name),
                limit=sql.Literal(limit),
            )

            logger.info(f"Executing query: {stmt.as_string(connection)}")  # Log the SQL query

            cursor.execute(stmt)
            result = cursor.fetchone()

        rowcount, = result
        logger.info(f"Rows counted for table {table_name}: {rowcount}")  # Log the result
        return rowcount
    except Exception as e:
        logger.error(f"Error counting rows: {e}")
        return -1


print(check_user_for_admin())
print(count_rows('users', 1))
print(count_rows('users', 10))


