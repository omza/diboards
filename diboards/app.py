import logging
import logging.handlers

import os
from sys import stdout

from flask import Flask

from database import db
from api import api
from api.boards import api as boards_ns
from api.users import api as users_ns
from api.tools import api as tools_ns

# Flask app instance
app = Flask(__name__, instance_relative_config=True)
log = logging.getLogger('diboardapi')

# App Configuration
# ------------------------------------------------------------------------------
def LoadAppConfiguration(flaskapp):
    
    # Load the default configuration
    flaskapp.config.from_object('config.default')
 
    # Load the configuration from the instance folder
    flaskapp.config.from_pyfile('secrets.py')
 
    # Load the file specified by the APP_CONFIG_FILE environment variable
    # Variables defined here will override those in the default configuration
    flaskapp.config.from_envvar('APP_CONFIG_FILE')
    pass

# Logging Configuraion
# ---------------------------------------------------------------------------------
def LoadLoggingConfiguration(flaskapp, rootlog):

    # formatter
    formatter = logging.Formatter('%(asctime)s | %(name)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s')

    #console handler    
    consolehandler = logging.StreamHandler(stdout)
    consolehandler.setFormatter(formatter)
    consolehandler.setLevel(flaskapp.config['DIBOARDS_LOGLEVEL_CONSOLE'])
    
    #file handler
    LOG_FILENAME = flaskapp.config['DIBOARDS_PATH_LOG'] + 'diboardsapi.log'
    filehandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, flaskapp.config['DIBOARDS_LOGMAXBYTE_FILE'], flaskapp.config['DIBOARDS_LOGBACKUPCOUNT_FILE'])
    filehandler.setFormatter(formatter)
    filehandler.setLevel(flaskapp.config['DIBOARDS_LOGLEVEL_FILE'])

    #overall log level
    loggerdebuglevel = min(filter(None, (flaskapp.config['DIBOARDS_LOGLEVEL_CONSOLE'], flaskapp.config['DIBOARDS_LOGLEVEL_FILE'])))    

    #diboards logger 
    rootlog.setLevel(loggerdebuglevel)
    rootlog.addHandler(consolehandler)
    rootlog.addHandler(filehandler)
    
    #werkzeug logger
    werkzeuglog = logging.getLogger('werkzeug')
    werkzeuglog.setLevel(loggerdebuglevel)
    werkzeuglog.addHandler(consolehandler)
    werkzeuglog.addHandler(filehandler)

    #flask-restplus logger
    flasklog = logging.getLogger('flask_restplus')
    flasklog.setLevel(loggerdebuglevel)
    flasklog.addHandler(consolehandler)
    flasklog.addHandler(filehandler)
    pass

def LogEnvironment(flaskapp, rootlog):
    if flaskapp.config['SERVER_NAME'] is not None:
        rootlog.debug('SERVER_NAME=' + flaskapp.config['SERVER_NAME'])
    else:
        rootlog.debug('SERVER_NAME=None') 
    
    rootlog.debug('HOST=' + flaskapp.config['HOST'])
    rootlog.debug('PORT=' + str(flaskapp.config['PORT']))
    rootlog.debug('DEBUG=' + str(flaskapp.config['DEBUG']))
    rootlog.debug('APP_CONFIG_FILE=' + os.environ.get('APP_CONFIG_FILE','No APP Config file'))
    rootlog.debug('SQLALCHEMY_DATABASE_URI=' + flaskapp.config['SQLALCHEMY_DATABASE_URI'])
    # Logging
    rootlog.debug('DIBOARDS_PATH_LOG=' + flaskapp.config['DIBOARDS_PATH_LOG'])
    rootlog.debug('DIBOARDS_LOGLEVEL_CONSOLE={!s}'.format(flaskapp.config['DIBOARDS_LOGLEVEL_CONSOLE']))
    rootlog.debug('DIBOARDS_LOGLEVEL_FILE={!s}'.format(flaskapp.config['DIBOARDS_LOGLEVEL_FILE']))


# startup App configuration/setting
# --------------------------------------------------------
if __name__ == '__main__':

    # Load Config
    LoadAppConfiguration(app)
    LoadLoggingConfiguration(app,log)

    # Initialize flask-restplus api
    # register di.boards api namespace
    api.add_namespace(boards_ns)
    api.add_namespace(users_ns)
    api.add_namespace(tools_ns)
    api.init_app(app)

    # Initialize SQL Alchemy
    db.init_app(app)
    
    # log environment
    LogEnvironment(app, log)

    # Make the WSGI interface available at the top level so wfastcgi can get it.
    wsgi_app = app.wsgi_app
    
    # run di.boards api app
    app.run(host=app.config['HOST'], port = app.config['PORT'])
