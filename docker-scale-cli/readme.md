```markdown
# Docker Scale CLI

A simple command-line interface (CLI) tool to scale Docker Compose services up or down and reload Nginx to update upstream servers.

## Features

- **Scale Services:** Easily scale the `app` service by specifying the number of replicas.
- **Automatic Nginx Reload:** Automatically reloads Nginx after scaling to ensure traffic is distributed across all replicas.
- **Error Handling:** Provides informative messages and handles errors gracefully.

## Prerequisites

- [Node.js](https://nodejs.org/) (v14 or later)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/docker-scale-cli.git
   cd docker-scale-cli
   ```

2. **Install Dependencies**

   ```bash
   npm install
   ```

## Usage

Start the CLI by running:

```bash
npm start
```

You will be presented with a menu:

```
? Select a task to perform:
❯ Scale 'app' service up
  Scale 'app' service down
  Exit
```

### Scale Up

1. Select **"Scale 'app' service up"**.
2. Enter the desired number of replicas greater than the current count.

### Scale Down

1. Select **"Scale 'app' service down"**.
2. Enter the desired number of replicas less than the current count.

### Exit

Select **"Exit"** to terminate the CLI.

## Project Structure

```
docker-scale-cli/
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

- **constants.mjs:** Defines menu choices.
- **mainMenu.mjs:** Entry point for the CLI application.
- **tasks/scaleService.mjs:** Handles scaling logic and Nginx reload.
- **utils/dockerHelpers.mjs:** Contains Docker-related helper functions.
- **utils/errorHandlers.mjs:** Manages error logging.

## Example Script

Here's an example bash script to scale up the `app` service and reload Nginx:

```bash
#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to display error messages
error_exit() {
  echo "Error: $1"
  exit 1
}

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
  error_exit "docker-compose is not installed. Please install it first."
fi

# Desired number of replicas
REPLICAS=7

# Scale the app service to the desired number of replicas
echo "Scaling the 'app' service to $REPLICAS replicas..."
docker-compose up -d --scale app=$REPLICAS --no-recreate

echo "Successfully scaled the 'app' service to $REPLICAS replicas."

# Reload Nginx to update upstream servers
echo "Reloading Nginx to update upstream servers..."
docker-compose exec nginx nginx -s reload

echo "Nginx reloaded successfully."

# Display currently running containers
echo "Currently running containers:"
docker ps
```

## Troubleshooting

- **Nginx Not Routing to New Replicas:**
  - Ensure the CLI successfully reloads Nginx after scaling.
  - Verify Nginx configuration correctly references the `app` service.

- **Permissions Issues:**
  - Ensure you have the necessary permissions to execute Docker commands and access Docker Compose files.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.
