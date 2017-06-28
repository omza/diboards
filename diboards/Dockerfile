FROM omza/alpine-nginx-py3-supervisor
MAINTAINER oliver@app-workshop.de

# ARGs & ENVs
# -------------------------------------------------------
ARG DIBOARDS_VERSION
ENV DIBOARDS_VERSION ${DIBOARDS_VERSION:-v0.1}
ARG DIBOARDS_BUILD
ENV DIBOARDS_BUILD ${DIBOARDS_BUILD:-0000.00.00.00.00}

ENV NGINX_VERSION 1.13.1
ENV NGINX_CONFIG /usr/src/app/deploy/nginx.prod.conf
ENV APP_CONFIG_FILE /usr/src/app/config/default.py

# dirs & volumes
# --------------------------------------------------------
RUN mkdir -p /usr/src/app \
	&& mkdir -p /usr/db \
	&& mkdir -p /usr/log \
	&& mkdir -p /tmp

WORKDIR /usr/src/app

COPY . /usr/src/app
RUN mv /usr/src/app/database/db.diboards /usr/db/db.diboards

VOLUME /usr/src/app/
VOLUME /usr/src/app/manage/static/
VOLUME /usr/db/
VOLUME /usr/log/
#COPY ./deploy/nginx.dev.conf /etc/nginx/nginx.conf

# Install requirements
# ----------------------------------------------------------
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Start & Stop
# -----------------------------------------------------------
EXPOSE 80 443
STOPSIGNAL SIGTERM
ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/usr/src/app/deploy/supervisord.conf"]