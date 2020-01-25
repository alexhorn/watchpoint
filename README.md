# Watchpoint

A network monitoring system for home networks. Scans your network for connected devices and identifies open ports, Bonjour and UPnP services and services with no or weak authentication. Designed to be easy to install and use.

## Installation

### Via Docker

You need to install [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/) first.

Then, create a `watchpoint` folder and put the following configuration into a `docker-compose.yml`:

```
version: '3.4'
services:
  app:
    image: alexhorn/watchpoint:latest
    restart: always
    volumes:
      - "/etc/watchpoint:/etc/watchpoint"
      - "/var/lib/watchpoint:/var/lib/watchpoint"
    network_mode: host
    environment:
      - WATCHPOINT_PORT=80
```

Now you can start it with `docker-compose up -d`. The web interface will be reachable at port 80.
