# https://github.com/alexhorn/docker-piler/tree/master/rootfs/etc/nginx

daemon off;

user www-data www-data;
error_log /dev/stderr;
pid /tmp/nginx.pid;

events {
  worker_connections 4096;
}

http {
  include /etc/nginx/mime.types;
  default_type application/octet-stream;

  server {
      listen ${WATCHPOINT_PORT} default_server;

      root /opt/watchpoint/frontend/build;
      index /index.html;

      location /api {
          include /etc/nginx/uwsgi_params;
          uwsgi_pass unix:/tmp/backend.sock;
      }

      location / {
          try_files $uri $uri/ /index.html;
      }
  }
}
