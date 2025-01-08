
# Nginx Load Balancer Readme

This folder contains the configuration and scripts for setting up an Nginx-based load balancer with dynamic backend management and logging.

---

## File Structure
```
nginx-lb/
├── Dockerfile           # Dockerfile to build the Nginx image
├── backend_map.conf     # Backend mapping configuration
├── nginx.conf           # Main Nginx configuration
└── watch.sh             # Script to reload Nginx on backend configuration changes
```

---

## Key Features

1. **Dynamic Backend Management**:
   - Uses a `map` directive in `backend_map.conf` to route requests based on the `internal_ip` cookie.
   - Default backend serves traffic when no cookie is present or matched.

2. **Logging**:
   - Logs requests using a custom log format including `internal_ip` from cookies.
   - Log details are stored in `/var/log/nginx/access.log`.

3. **Configuration Reload**:
   - The `watch.sh` script monitors `backend_map.conf` for changes and reloads Nginx automatically.

4. **Scalability**:
   - Works seamlessly with Docker Compose to load balance traffic across multiple replicas of the Python app.

---

## File Descriptions

### `Dockerfile`
- **Base Image**: Uses the official `nginx:latest` image.
- **Additions**:
  - Installs `inotify-tools` for file change monitoring.
  - Copies `nginx.conf` and `backend_map.conf` into the container.
  - Includes `watch.sh` to monitor and reload configurations.
- **Exposed Port**: `80` for HTTP traffic.

### `backend_map.conf`
- Defines the mapping of `internal_ip` cookies to specific backends.
- Default backend routes to `http://backend` when no specific mapping exists.

Example:
```nginx
map $cookie_internal_ip $backend {
    default "http://backend";  # Fallback backend
}
```

### `nginx.conf`
- Configures the Nginx server to:
  - Use `backend_map.conf` for backend selection.
  - Forward traffic to the `backend` upstream.
  - Log requests with the `internal_ip` cookie.
- Includes:
  - `proxy_pass` directive to dynamically route traffic.
  - Headers for request forwarding (`Host` and `X-Real-IP`).

### `watch.sh`
- A script to reload Nginx when `backend_map.conf` is modified.
- Uses `inotifywait` to monitor file changes and triggers a reload command.

---

## How to Build and Run

1. **Build the Docker Image**:
   ```bash
   docker build -t nginx-lb .
   ```

2. **Run the Container**:
   ```bash
   docker run -d -p 80:80 --name nginx-lb nginx-lb
   ```

3. **Monitor Logs**:
   ```bash
   docker logs -f nginx-lb
   ```

---

## Integration with Docker Compose

The `nginx` service can be included in a `docker-compose.yml` file to act as a reverse proxy for the `app` service.

Example:
```yaml
nginx:
  build:
    context: ./nginx-lb
    dockerfile: Dockerfile
  ports:
    - "80:80"
  depends_on:
    - app
```

---

## Notes
- Ensure `backend_map.conf` is correctly configured to reflect the actual backend services.
- Logs are stored in the container at `/var/log/nginx/access.log`.
- Modify the resolver settings in `nginx.conf` if using dynamic DNS for backends.

