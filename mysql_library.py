# BEGIN (https://realpython.com/python-sql-libraries/#sqlite)
import mysql.connector
import time
import yaml

from mysql.connector import Error


def create_connection(host_name, user_name, user_password, host_port, host_database):
    connection = None

    try:

        connection = mysql.connector.connect(

            host=host_name,

            database=host_database,

            port=host_port,

            user=user_name,

            passwd=user_password

        )

        print("Connected to MySQL DB successfully")

    except Error as e:

        print(f"The error '{e}' occurred")

    return connection

connection = ""

with open(r'config.yaml') as file:
    document = yaml.full_load(file)
    connection = create_connection(document.get("hostname"), document.get("username"), document.get("password"), document.get("port"), document.get("database"))


async def execute_query(connection, query):
    cursor = connection.cursor()

    try:

        cursor.execute(query)

        connection.commit()

        print("Query executed successfully")

    except Error as e:

        print(f"The error '{e}' occurred")


async def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")



# END (https://realpython.com/python-sql-libraries/#sqlite)
