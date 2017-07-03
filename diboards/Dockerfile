FROM omza/alpine-nginx-py3-supervisor
MAINTAINER oliver@app-workshop.de

# ARGs & ENVs
# -------------------------------------------------------
ENV NGINX_CONFIG /usr/src/app/deploy/nginx.prod.conf
ENV NGINX_SSL_KEY /certs/default.key
ENV NGINX_SSL_CRT /certs/default.crt

ENV DIBOARDS_VERSION v0.1
ENV DIBOARDS_CONFIG_FILE /usr/src/app/config/default.py
ENV DIBOARDS_SECRET_FILE /usr/src/app/config/secrets.py

# dirs & volumes
# --------------------------------------------------------
RUN mkdir -p /usr/src/app \
	&& mkdir -p /usr/db \
	&& mkdir -p /usr/log \
	&& mkdir -p /tmp \
	&& mkdir -p /certs

WORKDIR /usr/src/app

COPY . /usr/src/app
RUN mv /usr/src/app/database/db.diboards /usr/db/db.diboards

VOLUME /usr/src/app/
VOLUME /usr/db/
VOLUME /usr/log/

# Install requirements
# ----------------------------------------------------------
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Start & Stop
# -----------------------------------------------------------
EXPOSE 80 443
STOPSIGNAL SIGTERM
ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/usr/src/app/deploy/supervisord.conf"]