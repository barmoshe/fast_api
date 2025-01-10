import os
import socket
import signal
import sys
import time
from datetime import datetime

from fastapi import FastAPI, Request, Response, Cookie
from fastapi.staticfiles import StaticFiles
import mysql.connector
from mysql.connector import Error

app = FastAPI()


# Mount the static files directory
app.mount("/frontend", StaticFiles(directory="static", html=True), name="static")

# Database Configuration (from environment variables)
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = int(os.getenv("DATABASE_PORT", "3306"))
DB_USER = os.getenv("DATABASE_USER", "root")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "example")
DB_NAME = os.getenv("DATABASE_NAME", "whist_db")

# Path to the Nginx backend map file
BACKEND_MAP_FILE = "/etc/nginx/conf.d/backend_map.conf"

# Global variable to store the server's IP
server_ip = None


def get_server_ip():
    """Retrieve the server's IP address."""
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.error:
        return "unknown"


def check_ip_exists(ip):
    """Check if the given IP exists in the backend_map.conf file."""
    try:
        with open(BACKEND_MAP_FILE, "r") as file:
            data = file.readlines()
        for line in data:
            if f'"{ip}"' in line:
                return True
        return False
    except FileNotFoundError:
        print(f"Backend map file {BACKEND_MAP_FILE} not found.")
        return False
    except Exception as e:
        print(f"Error checking IP existence: {e}")
        return False


def update_server_ip(ip):
    """Add the server's IP to the backend_map.conf file."""
    try:
        if check_ip_exists(ip):
            print(f"IP {ip} already exists in {BACKEND_MAP_FILE}.")
            return
        with open(BACKEND_MAP_FILE, "r") as file:
            data = file.readlines()
        # Insert the new IP mapping before the closing brace
        insert_index = None
        for i, line in enumerate(data):
            if line.strip() == "}":
                insert_index = i
                break
        if insert_index is not None:
            data.insert(insert_index, f'    "{ip}" "http://{ip}:8000";\n')
            with open(BACKEND_MAP_FILE, "w") as file:
                file.writelines(data)
        else:
            print(f"Closing brace not found in {BACKEND_MAP_FILE}.")
    except Exception as e:
        print(f"Error updating client IP: {e}")


def remove_server_ip(ip):
    """Remove the server's IP from the backend_map.conf file."""
    # wait 1 ms per las t 2 digits of the ip address
    time.sleep(int(ip.split(".")[-1]) / 10)
    try:
        with open(BACKEND_MAP_FILE, "r") as file:
            data = file.readlines()
        new_data = [line for line in data if f'"{ip}"' not in line]
        with open(BACKEND_MAP_FILE, "w") as file:
            file.writelines(new_data)
    except FileNotFoundError:
        print(f"Backend map file {BACKEND_MAP_FILE} not found.")
    except Exception as e:
        print(f"Error removing client IP: {e}")


def signal_handler(signum, frame):
    """Handle termination signals to perform cleanup."""
    print(f"Received signal {signum}. Shutting down gracefully...")
    if server_ip:
        remove_server_ip(server_ip)
    sys.exit(0)


# Register signal handlers for graceful shutdown
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


def get_db_connection():
    """Establish a connection to the MySQL database."""
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


def initialize_counter():
    """Initialize the global_counter table."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS global_counter (
                    id INT PRIMARY KEY,
                    value INT NOT NULL
                )
                """
            )
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
    """Initialize the access_log table."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS access_log (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    client_ip VARCHAR(255) NOT NULL,
                    server_ip VARCHAR(255) NOT NULL,
                    access_time DATETIME NOT NULL,
                    action VARCHAR(255) NOT NULL,
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


def increment_global_counter():
    """Increment the global counter atomically."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE global_counter SET value = value + 1 WHERE id = 1")
            connection.commit()
            cursor.execute("SELECT value FROM global_counter WHERE id = 1")
            counter = cursor.fetchone()[0]
            return counter
        except Error as e:
            print(f"Database error in increment_global_counter: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    return None


def set_internal_ip_cookie(response: Response, internal_ip: str):
    """Set a cookie for the internal IP."""
    response.set_cookie(
        key="internal_ip",
        value=internal_ip,
        max_age=300,  # 5 minutes
        httponly=True,
    )


def record_access_log(
    client_ip: str,
    server_ip: str,
    access_time: datetime,
    counter: int,
    action="increment",
):
    """Record the access details in the logs folder."""
    log_file = "logs/access.log"
    with open(log_file, "a") as file:
        file.write(f"{access_time} - {client_ip} - {server_ip} - {counter}\n")
    """Record the access details in the access_log table."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO access_log (client_ip, server_ip, access_time, counter, action)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (client_ip, server_ip, access_time, counter, action),
            )
            connection.commit()
        except Error as e:
            print(f"Database error in record_access_log: {e}")
        finally:
            cursor.close()
            connection.close()


@app.get("/")
async def increment_counter(
    request: Request, response: Response, internal_ip: str = Cookie(None)
):
    """Main route handler to increment counter and log access."""
    client_ip = request.client.host
    access_time = datetime.now()

    # Get the server's IP address
    current_server_ip = get_server_ip()

    # Step 1: Increment the counter
    counter = increment_global_counter()
    if counter is None:
        return {"error": "Failed to increment counter in the database"}

    # Step 2: Create a cookie for the internal IP
    set_internal_ip_cookie(response, current_server_ip)

    # Step 3: Record the access log
    record_access_log(client_ip, current_server_ip, access_time, counter)

    return {"server_internal_ip": current_server_ip, "counter": counter}


@app.get("/showcount")
async def show_count(request: Request):
    """Endpoint to show the current global counter value."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT value FROM global_counter WHERE id = 1")
            result = cursor.fetchone()
            record_access_log(
                request.client.host,
                server_ip,
                datetime.now(),
                result[0],
                action="show count",
            )
            if result:
                counter = result[0]
                return {"global_counter": counter}
            else:
                print("Global counter not found.")
                return {"error": "Global counter not found"}
        except Error as e:
            print(f"Database error: {e}")
            return {"error": "Failed to retrieve counter"}
        finally:
            cursor.close()
            connection.close()
    else:
        return {"error": "Database connection failed"}


@app.get("/showlogs")
async def show_logs(request: Request):
    """Endpoint to show the latest 10 access logs."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM access_log ORDER BY access_time DESC ")
            logs = cursor.fetchall()
            return {"access_logs": logs}
        except Error as e:
            print(f"Database error: {e}")
            return {"error": "Failed to retrieve logs"}
        finally:
            record_access_log("localhost", server_ip, datetime.now(), -1, action="show logs")
            cursor.close()
            connection.close()
    else:
        return {"error": "Database connection failed"}


@app.on_event("startup")
def initialize_app():
    """Initialize the application by setting up the database and updating the backend map."""
    global server_ip
    print("Initializing application...")
    server_ip = get_server_ip()
    initialize_counter()
    initialize_access_log()
    update_server_ip(server_ip)
    print("Application started.")


# Initialize the application on startup
initialize_app()
