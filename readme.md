
# Whist Assignment V2

This is version 2 (V2) of the Whist Assignment, a containerized web application project. This version introduces streamlined configurations by removing unused features like dynamic backend mapping and simplifies the overall design while retaining core functionality.

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
   - Nginx acts as a reverse proxy and handles cookie-based sticky sessions directly in the configuration without additional mapping files.

4. **Scalability**:
   - Pre-configured with 3 replicas of the application container.
   - A Bash script (`scale_app.sh`) and a CLI tool allow scaling up/down to a specified number of replicas.

5. **Simplified Architecture**:
   - Removed unnecessary files (`backend_map.conf`, `watch.sh`) and reduced complexity in Nginx configuration.

---

## File Structure
```
whist_assignment_v2/
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
├── nginx-lb
│   ├── Dockerfile       # Dockerfile for Nginx
│   ├── nginx.conf       # Nginx server configuration
├── readme.md            # Main README file
├── scale_app.sh         # Bash script for scaling application replicas
└── docker-scale-cli
    ├── constants.mjs
    ├── mainMenu.mjs
    ├── package-lock.json
    ├── package.json
    ├── tasks
    │   └── scaleService.mjs
    └── utils
        ├── dockerHelpers.mjs
        └── errorHandlers.mjs
```

---

## How to Set Up

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd whist_assignment_v2
   ```

2. **Build and Start Containers**:
   ```bash
   docker-compose up --build
   ```

3. **Access the Application**:
   - Open a browser and navigate to `http://localhost/`.
   - Use `/showcount` to view the global counter.

4. **Scale Application**:
   - **Using Bash Script**:
     Run the `scale_app.sh` script to change the number of application replicas:
     ```bash
     ./scale_app.sh
     ```
   - **Using CLI Tool**:
     Navigate to the CLI directory and start the CLI:
     ```bash
     cd docker-scale-cli
     npm install
     npm start
     ```
     Follow the interactive prompts to scale the `app` service up or down.

---

## Key Changes in V2

1. **Simplified Backend Management**:
   - Removed the `backend_map.conf` file.
   - Cookie-based sticky sessions are now directly handled in `nginx.conf`.

2. **Removed Dynamic Configuration Reload**:
   - `watch.sh` script and `inotify-tools` dependency have been removed.
   - Backend configuration is now static and simplified.

3. **Streamlined Nginx Configuration**:
   - Directly proxies requests based on the presence of the `internal_ip` cookie.
   - Reduced overhead while maintaining functionality.

4. **Retained Core Features**:
   - Global counter functionality and logging remain unchanged.
   - Application scaling and persistence are preserved.

---

## Custom Scripts

### `scale_app.sh`
- Bash script to scale the `app` service to a specified number of replicas.

### CLI Tool
- A CLI tool to scale the `app` service up or down and automatically reload Nginx to update upstream servers.
- **Usage**:
  ```bash
  cd docker-scale-cli
  npm install
  npm start
  ```
- **Documentation**: [Docker Scale CLI README](./docker-scale-cli/README.md)

---

## Notes

- Ensure Docker and Docker Compose are installed.
- Verify MySQL and application logs for debugging.
- The `nginx.conf` file now directly manages cookie-based sticky sessions, simplifying configuration management.
```

---
