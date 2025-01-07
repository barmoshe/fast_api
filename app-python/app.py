from fastapi import FastAPI, Request, Response, Cookie
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import os

app = FastAPI()

# Database Configuration (from environment variables)
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = os.getenv("DATABASE_PORT", "3306")
DB_USER = os.getenv("DATABASE_USER", "root")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "example")
DB_NAME = os.getenv("DATABASE_NAME", "whist_db")


# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# Ensure the counter table exists
def initialize_counter():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Create a counter table if it doesn't exist
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS global_counter (
                id INT PRIMARY KEY,
                value INT NOT NULL
            )
            """
            )
            # Initialize the counter if it doesn't already exist
            cursor.execute(
                "INSERT IGNORE INTO global_counter (id, value) VALUES (1, 0)"
            )
            connection.commit()
        except Error as e:
            print(f"Database error during initialization: {e}")
        finally:
            cursor.close()
            connection.close()


def initialize_access_log():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Create a counter table if it doesn't exist
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS access_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                client_ip VARCHAR(255) NOT NULL,
                server_ip VARCHAR(255) NOT NULL,
                access_time DATETIME NOT NULL,
                counter INT NOT NULL
            )
            """
            )
            connection.commit()
        except Error as e:
            print(f"Database error during initialization: {e}")
        finally:
            cursor.close()
            connection.close()


# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# 1. Increment the counter and save it to the DB
def increment_global_counter():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Increment the counter atomically
            cursor.execute("UPDATE global_counter SET value = value + 1 WHERE id = 1")
            connection.commit()

            # Retrieve the updated counter value
            cursor.execute("SELECT value FROM global_counter WHERE id = 1")
            counter = cursor.fetchone()[0]
            return counter
        except Error as e:
            print(f"Database error in increment_global_counter: {e}")
            return None
        finally:
            cursor.close()
            connection.close()


# 2. Create a cookie for the internal IP
def set_internal_ip_cookie(response: Response, internal_ip: str):
    response.set_cookie(
        key="internal_ip",
        value=internal_ip,
        max_age=300,  # 5 minutes
        httponly=True,
    )


# 3. Record client and server details in the access_log table
def record_access_log(
    client_ip: str, server_ip: str, access_time: datetime, counter: int
):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Log the access in the access_log table
            cursor.execute(
                """
            INSERT INTO access_log (client_ip, server_ip, access_time, counter)
            VALUES (%s, %s, %s, %s)
            """,
                (client_ip, server_ip, access_time, counter),
            )
            connection.commit()
        except Error as e:
            print(f"Database error in record_access_log: {e}")
        finally:
            print("Access logged successfully")
            cursor.close()
            connection.close()


# Main route handler
@app.get("/")
async def increment_counter(
    request: Request, response: Response, internal_ip: str = Cookie(None)
):
    client_ip = request.client.host
    server_ip = os.getenv("HOSTNAME", "unknown")
    access_time = datetime.now()

    # Step 1: Increment the counter
    counter = increment_global_counter()
    if counter is None:
        return {"error": "Failed to increment counter in the database"}

    # Step 2: Create a cookie for the internal IP
    set_internal_ip_cookie(response, server_ip)

    # Step 3: Record the access log
    record_access_log(client_ip, server_ip, access_time, counter)

    return {"server_internal_ip": server_ip, "counter": counter}


@app.get("/showcount")
async def show_count():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Retrieve the counter value from the database
            cursor.execute("SELECT value FROM global_counter WHERE id = 1")
            counter = cursor.fetchone()[0]

        except Error as e:
            print(f"Database error: {e}")
            return {"error": "Failed to retrieve counter"}
        finally:
            cursor.close()
            connection.close()

        return {"global_counter": counter}
    else:
        return {"error": "Database connection failed"}


@app.get("/showlogs")
async def show_logs():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Retrieve the access logs from the database
            cursor.execute(
                "SELECT * FROM access_log ORDER BY access_time DESC LIMIT 10"
            )
            logs = cursor.fetchall()

        except Error as e:
            print(f"Database error: {e}")
            return {"error": "Failed to retrieve logs"}
        finally:
            cursor.close()
            connection.close()

        return {"access_logs": logs}
    else:
        return {"error": "Database connection failed"}


# Initialize tables
initialize_counter()
initialize_access_log()
