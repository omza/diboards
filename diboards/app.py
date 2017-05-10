# Import
import os
import logging
from sys import stdout
from flask import Flask
from api import api
from database import db


# Flask app instance
app = Flask(__name__, instance_relative_config=True)

# Logging
# --------------------------------------------------------------------------------------------------------------------

# formatter
formatter = logging.Formatter('%(asctime)s | %(name)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s')

#console handler    
consolehandler = logging.StreamHandler(stdout)
consolehandler.setFormatter(formatter)
consolehandler.setLevel(logging.DEBUG)
    
#app logger
log = logging.getLogger('diboardapi')
log.setLevel(logging.DEBUG)
log.addHandler(apphandler)
    
#werkzeug logger
werkzeuglog = logging.getLogger('werkzeug')
werkzeuglog.setLevel(logging.DEBUG)
werkzeuglog.addHandler(apphandler)

# startup App configuration/setting
if __name__ == '__main__':

    # Load the default configuration
    app.config.from_object('config.default')
 
    # Load the configuration from the instance folder
    app.config.from_pyfile('secrets.py')
 
    # Load the file specified by the APP_CONFIG_FILE environment variable
    # Variables defined here will override those in the default configuration
    app.config.from_envvar('APP_CONFIG_FILE')

    # Initialize flask-restplus api
    api.init_app(app)

    # Initialize SQL Alchemy
    db.init_app(app)
    
    # log environment
    if app.config['SERVER_NAME'] is not None:
        log.debug('SERVER_NAME=' + app.config['SERVER_NAME'])
    else:
        log.debug('SERVER_NAME=None') 
    log.debug('HOST=' + app.config['HOST'])
    log.debug('PORT=' + str(app.config['PORT']))
    log.debug('DEBUG=' + str(app.config['DEBUG']))
    log.debug('APP_CONFIG_FILE=' + os.environ.get('APP_CONFIG_FILE','No APP Config file'))
    log.debug('SQLALCHEMY_DATABASE_URI=' + app.config['SQLALCHEMY_DATABASE_URI'])

    # Make the WSGI interface available at the top level so wfastcgi can get it.
    wsgi_app = app.wsgi_app
    
    # run di.boards api app
    app.run(host=app.config['HOST'], port = app.config['PORT'])
