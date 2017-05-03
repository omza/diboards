FROM python:3.6.1-alpine
MAINTAINER oliver@app-workshop.de

RUN mkdir -p /usr/src/app
	&& mkdir -p /usr/qr
	&& mkdir -p /usr/incomming
	&& mkdir -p /usr/outgoing

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

VOLUME /usr/src/app/
VOLUME /usr/qr/
VOLUME /usr/incomming/
VOLUME /usr/outgoing/

ENV APP_CONFIG_FILE /usr/src/app/config/default.py


EXPOSE 5000
CMD [ "python", "app.py" ] 