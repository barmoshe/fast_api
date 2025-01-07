#!/bin/bash

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
  echo "docker-compose is not installed. Please install it first."
  exit 1
fi

# Scale the app service to 5 replicas
echo "Scaling the 'app' service to 5 replicas..."
docker-compose up -d --scale app=5 --no-recreate

if [ $? -eq 0 ]; then
  echo "Successfully scaled the 'app' service to 5 replicas."
else
  echo "Failed to scale the 'app' service. Check the logs for more details."
  exit 1
fi

echo "Currently running containers:"
docker ps
