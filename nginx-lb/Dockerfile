FROM nginx:latest

# Install inotify-tools
RUN apt-get update && \
    apt-get install -y inotify-tools && \
    rm -rf /var/lib/apt/lists/*

# Copy the Nginx server configuration to the appropriate directory
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY backend_map.conf /etc/nginx/conf.d/backend_map.conf

# Add a script to watch for changes and reload Nginx
COPY watch.sh /watch.sh
RUN chmod +x /watch.sh

EXPOSE 80

CMD ["/watch.sh"]
