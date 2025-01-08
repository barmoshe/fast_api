#!/bin/bash

set -e

LOG_FILE="scale_app.log"

error_exit() {
  echo "Error: $1" | tee -a "$LOG_FILE"
  exit 1
}

if ! command -v docker-compose &> /dev/null; then
  error_exit "docker-compose is not installed. Please install it first."
fi

REPLICAS=7

echo "Scaling the 'app' service to $REPLICAS replicas..." | tee -a "$LOG_FILE"
docker-compose up -d --scale app=$REPLICAS --no-recreate 2>&1 | tee -a "$LOG_FILE"

echo "Successfully scaled the 'app' service to $REPLICAS replicas." | tee -a "$LOG_FILE"

echo "Reloading Nginx to update upstream servers..." | tee -a "$LOG_FILE"
docker-compose exec nginx nginx -s reload 2>&1 | tee -a "$LOG_FILE"

echo "Nginx reloaded successfully." | tee -a "$LOG_FILE"

echo "Currently running containers:" | tee -a "$LOG_FILE"
docker ps | tee -a "$LOG_FILE"
