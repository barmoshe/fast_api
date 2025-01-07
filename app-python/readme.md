```markdown
# Python and Docker Components Readme

This application is a Python-based FastAPI web service integrated with MySQL for data storage. Docker is used for containerization, ensuring easy deployment and scalability.

---

## Python Application (`app.py`)

### Key Features:
1. **Counter Management**: 
   - The root route (`/`) increments a global counter stored in the MySQL database.
   - Counter updates are handled atomically to prevent race conditions.

2. **Logging**:
   - Logs client requests with details like client IP, server IP, access time, and counter value into the `access_log` table.

3. **Cookie Management**:
   - Sets a cookie named `internal_ip` on the client for maintaining server stickiness.

4. **Routes**:
   - `GET /`: Increments the counter, sets a cookie, and logs the request.
   - `GET /showcount`: Returns the current value of the global counter.
   - `GET /showlogs`: Displays the latest 10 access logs.

### Database Setup:
- **Global Counter Table**:
   - Table: `global_counter`
   - Columns: `id` (Primary Key), `value` (Integer).

- **Access Logs Table**:
   - Table: `access_log`
   - Columns: `id` (Primary Key), `client_ip`, `server_ip`, `access_time`, `counter`.

### Environment Variables:
- `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_NAME`.

---

## Docker Components

### Dockerfile
The `Dockerfile` for the Python application uses a lightweight Python image, installs dependencies from `requirements.txt`, copies static files and application code, and runs the FastAPI app with `uvicorn`.

---

### Docker Compose
The `docker-compose.yml` file orchestrates the following services:
1. **Database**:
   - MySQL 8.0 with persistent volumes for data and logs.
   - Pre-configured with health checks to ensure readiness.

2. **Python App**:
   - Builds from the provided `Dockerfile`.
   - Environment variables configure the database connection.
   - Logs are mapped to the host machine for persistence.

= Static Files
- **Static Files**: Served under the `/frontend` route for serving client assets like `index.html`.

--- 

### Key Notes:
- Ensure all environment variables are correctly set for the application and database.
- Use `docker-compose` for seamless multi-service orchestration and scaling.
```