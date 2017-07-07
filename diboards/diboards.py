# imports & globals
# -------------------------------------------------------------------------------
import os
from sys import stdout

from flask import Flask
from flask_cors import CORS, cross_origin

from database import db
from api import diboardsapi

import logging
import logging.handlers

# Flask app instance
app = Flask(__name__)
CORS(app)

# App Configuration
# ------------------------------------------------------------------------------
    
# Load the default configuration
app.config.from_object('config.default')
 
# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_envvar('DIBOARDS_CONFIG_FILE')

# Load the secrets configuration from the instance folder
if os.path.isfile('/secrets/secrets.py'):
    app.config.from_pyfile('/secrets/secrets.py', silent=True)
else:
    app.config.from_object('config.secrets')

#Add diboardsversion from buildinfo
app.config['DIBOARDS_VERSION']=os.environ.get('DIBOARDS_VERSION')


# Logging Configuraion
# ---------------------------------------------------------------------------------
# formatter
formatter = logging.Formatter('%(asctime)s | %(name)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s')

#console handler    
consolehandler = logging.StreamHandler(stdout)
consolehandler.setFormatter(formatter)
consolehandler.setLevel(app.config['DIBOARDS_LOGLEVEL_CONSOLE'])
    
#file handler
LOG_FILENAME = app.config['DIBOARDS_PATH_LOG'] + 'diboardsapi.log'
filehandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, app.config['DIBOARDS_LOGMAXBYTE_FILE'], app.config['DIBOARDS_LOGBACKUPCOUNT_FILE'])
filehandler.setFormatter(formatter)
filehandler.setLevel(app.config['DIBOARDS_LOGLEVEL_FILE'])

#overall log level
loggerdebuglevel = min(filter(None, (app.config['DIBOARDS_LOGLEVEL_CONSOLE'], app.config['DIBOARDS_LOGLEVEL_FILE'])))    

#diboards logger
log = logging.getLogger('diboardapi') 
log.setLevel(loggerdebuglevel)
log.addHandler(consolehandler)
log.addHandler(filehandler)

#flask-restplus logger
flasklog = logging.getLogger('flask_restplus')
flasklog.setLevel(loggerdebuglevel)
flasklog.addHandler(consolehandler)
flasklog.addHandler(filehandler)


# register blueprints api and manage
# --------------------------------------------------------
app.register_blueprint(diboardsapi)

# Initialize SQL Alchemy
# --------------------------------------------------------
db.init_app(app)

# log App configuration/setting  if in debug mode
# --------------------------------------------------------
if app.debug:
    for key, value in app.config.items():
        log.debug('{} = {!s}'.format(key, value))


# main
# -----------------------------------------------------------
if __name__ == '__main__':
    
    # run di.boards api app
    if app.config['SERVER_NAME'] is not None:
        app.run()
    else:
        app.run(host=app.config['HOST'], port = app.config['PORT'])
