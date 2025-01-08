```markdown
# Whist Assignment

This project demonstrates a containerized web application using **FastAPI**, **MySQL**, and **Nginx**. It leverages **Docker Compose** for multi-container orchestration and scalability.

---

## Features

1. **Web Application**:
   - Built with Python using FastAPI.
   - Provides two routes:
     - `GET /`: Increments a global counter stored in MySQL, sets a 5-minute cookie, and logs request details (client IP, server IP, timestamp) to a database table (`access_log`).
     - `GET /showcount`: Returns the current value of the global counter.

2. **Database**:
   - MySQL container stores the global counter and access logs.
   - Data and logs are retained on the host for persistence.

3. **Load Balancing**:
   - Nginx container acts as a reverse proxy and load balancer.
   - Supports cookie-based stickiness to ensure requests from the same client are routed to the same backend server for 5 minutes.

4. **Scalability**:
   - Pre-configured with 3 replicas of the application container.
   - A CLI tool and a Bash script allow scaling up/down to a specified number of replicas.

5. **Persistence**:
   - Application logs and database data are mapped to the host machine to ensure data persistence.

---

## File Structure
```
whist_assignment/
├── DB
│   ├── data             # MySQL data directory
│   ├── init.sql         # Initial SQL script to set up the database
│   └── logs             # MySQL log directory
├── app-python
│   ├── Dockerfile       # Dockerfile for the FastAPI app
│   ├── app.py           # Python application source code
│   ├── logs             # Directory to store application logs
│   ├── requirements.txt # Python dependencies
│   └── static           # Static assets (e.g., index.html)
├── docker-compose.yml   # Docker Compose configuration
├── docker-scale-cli
│   ├── constants.mjs
│   ├── mainMenu.mjs
│   ├── package-lock.json
│   ├── package.json
│   ├── tasks
│   │   └── scaleService.mjs
│   └── utils
│       ├── dockerHelpers.mjs
│       └── errorHandlers.mjs
├── nginx-lb
│   ├── Dockerfile       # Dockerfile for Nginx
│   ├── backend_map.conf # Backend configuration for sticky sessions
│   ├── nginx.conf       # Nginx server configuration
│   └── watch.sh         # Script to reload Nginx on config changes
├── readme.md            # Main README file
├── scale_app.sh         # Bash script for scaling application replicas
└── docker-scale-cli/README.md # CLI Tool Documentation
```

---

## How to Set Up

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd whist_assignment
   ```

2. **Build and Start Containers**:
   ```bash
   docker-compose up --build
   ```

3. **Access the Application**:
   - Open a browser and navigate to `http://localhost/`.
   - Use `/showcount` to view the global counter.

4. **Scale Application**:
   - Use the CLI tool or the Bash script to scale the `app` service.
   - **Using the CLI Tool**:
     ```bash
     cd docker-scale-cli
     npm install
     npm start
     ```
   - **Using the Bash Script**:
     ```bash
     ./scale_app.sh
     ```

---

## Key Components

### Docker Compose

- **Services**:
  1. **Database (MySQL)**:
     - Stores the global counter and logs.
     - Data and logs are retained on the host under `DB/`.
  2. **Application**:
     - Python-based FastAPI app running on `uvicorn`.
     - Logs are mapped to the host under `app-python/logs/`.
  3. **Nginx**:
     - Acts as a reverse proxy and load balancer.
     - Supports cookie-based sticky sessions using `internal_ip`.

- **Configuration**:
  - Defined in `docker-compose.yml` to orchestrate the services.

### Scaling

- The application is pre-configured with 3 replicas.
- Scale using:
  - **CLI Tool**: [Docker Scale CLI](./docker-scale-cli/README.md)
  - **Bash Script**:
    ```bash
    ./scale_app.sh
    ```

---

## Key Features

1. **Sticky Sessions**:
   - Nginx routes requests based on the `internal_ip` cookie to maintain session stickiness.

2. **Persistence**:
   - Database data and logs are retained under `DB/`.
   - Application logs are retained under `app-python/logs/`.

3. **Dynamic Configuration Reload**:
   - Nginx automatically reloads configurations when `backend_map.conf` is updated using `watch.sh`.

---

## Custom Scripts

### `scale_app.sh`
- Bash script to scale the `app` service to a specified number of replicas.

### CLI Tool
- A CLI tool to scale the `app` service up or down. [Read more](./docker-scale-cli/README.md)

---

## Notes

- Ensure Docker and Docker Compose are installed.
- Verify MySQL and application logs for debugging.
- Update the Nginx backend map (`backend_map.conf`) as needed for custom routing rules.
```

