# build frontend

FROM node:12-alpine AS frontend

WORKDIR /tmp/frontend

# add package.json first so the layer containing all dependencies can be cached
# use yarn because npm shows weird errors (npm ERR! Maximum call stack size exceeded)
ADD ./frontend/package*.json ./frontend/yarn.lock ./
RUN yarn install

ADD ./frontend ./
RUN yarn build

# build and package backend
# as per https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04

FROM debian:buster-slim

# add piwheels repository containing prebuilt wheels for raspberry pi to reduce compilation times
ADD docker/pip.conf /etc/pip.conf
# install supervisor from pip because the debian image depends on python2
# setuptools is required by supervisor, libpython3.7 is required by uwsgi, libxslt1.1 is required by lxml
RUN apt update -y && \
    apt install -y --no-install-recommends python3 python3-pip libpython3.7 libxslt1.1 nginx-light gettext-base iproute2 && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir uwsgi supervisor setuptools

WORKDIR /opt/watchpoint

# add requirements.txt first so the layer containing all dependencies can be cached
ADD requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

ADD . ./
COPY --from=frontend /tmp/frontend/build ./frontend/build

ENV WATCHPOINT_PORT=80
ENV WATCHPOINT_CONFIG_FILE=/etc/watchpoint/config.ini
# required to be able to print() into the docker logs
# as per https://github.com/Supervisor/supervisor/issues/893
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ./docker/start.sh
