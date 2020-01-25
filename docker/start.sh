# generate nginx config
envsubst '${WATCHPOINT_PORT}' < ./docker/nginx.conf.tpl > ./docker/nginx.conf

# copy config if necessary
if [ ! -f $WATCHPOINT_CONFIG_FILE ]; then
    cp ./config.ini.tpl $WATCHPOINT_CONFIG_FILE
fi

# fix permissions
chown www-data:www-data /etc/watchpoint
chown www-data:www-data /var/lib/watchpoint

# give python the capability to use raw sockets
# (doing this in the Dockerfile would create a full copy of the binary)
setcap cap_net_raw+ep /usr/bin/python3.7

# start supervisor
exec supervisord -c ./docker/supervisord.conf
