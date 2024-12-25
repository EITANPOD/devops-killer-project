FROM nginx:alpine

# Create necessary directories
RUN mkdir -p /usr/share/nginx/html/static/css \
    && mkdir -p /usr/share/nginx/html/static/js

# Copy static files
COPY static/ /usr/share/nginx/html/static/
COPY index.html /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80