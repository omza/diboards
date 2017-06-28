#!/bin/sh
# diboard startsript to configure nginx environment 
# depending on os environment vars
# retrieve env vars
echo "Check OS Environment Vars..."
printenv
nginxconfigfile = $(NGINX_CONFIG)
echo $nginxconfigfile
# check config file - abort if not there
# copy config file - abort on error
mv /usr/src/app/deploy/nginx.dev.conf /etc/nginx/nginx.conf
# start supervisor
supervisord --nodaemon --configuration /usr/src/app/deploy/supervisord.conf