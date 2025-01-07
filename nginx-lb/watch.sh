#!/bin/bash

# Start Nginx in the background
nginx -g 'daemon off;' &

# Watch for changes in backend_map.conf
while inotifywait -e modify /etc/nginx/conf.d/backend_map.conf; do
    echo "backend_map.conf changed, reloading Nginx..."
    nginx -s reload
done
