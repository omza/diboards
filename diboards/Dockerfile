FROM python:3.6.1-alpine
MAINTAINER oliver@app-workshop.de

RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/qr 
RUN mkdir -p /usr/incomming
RUN mkdir -p /usr/outgoing
RUN mkdir -p /usr/db

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
COPY db.diboards /usr/db/db.diboards
RUN rm db.diboards

VOLUME /usr/src/app/
VOLUME /usr/qr/
VOLUME /usr/incomming/
VOLUME /usr/outgoing/
VOLUME /usr/db/

ENV APP_CONFIG_FILE /usr/src/app/config/default.py

EXPOSE 5000
CMD [ "python", "app.py" ] 