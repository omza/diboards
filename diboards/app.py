import os
import logging
import logging.handlers
from sys import stdout
from flask import Flask
from api import api
from database import db

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
def LoadLoggingConfiguration(flaskapp, logger):

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

    #root logger
    loggerdebuglevel = min(filter(None, (flaskapp.config['DIBOARDS_LOGLEVEL_CONSOLE'], flaskapp.config['DIBOARDS_LOGLEVEL_FILE']))) 

    logger.setLevel(loggerdebuglevel)
    logger.addHandler(consolehandler)
    logger.addHandler(filehandler)
    
    #werkzeug logger
    werkzeuglog = logging.getLogger('werkzeug')
    werkzeuglog.setLevel(loggerdebuglevel)
    logger.addHandler(consolehandler)
    logger.addHandler(filehandler)
    pass

def LogEnvironment(flaskapp, logger):
    if flaskapp.config['SERVER_NAME'] is not None:
        logger.debug('SERVER_NAME=' + flaskapp.config['SERVER_NAME'])
    else:
        logger.debug('SERVER_NAME=None') 
    logger.debug('HOST=' + flaskapp.config['HOST'])
    logger.debug('PORT=' + str(flaskapp.config['PORT']))
    logger.debug('DEBUG=' + str(flaskapp.config['DEBUG']))
    logger.debug('APP_CONFIG_FILE=' + os.environ.get('APP_CONFIG_FILE','No APP Config file'))
    logger.debug('SQLALCHEMY_DATABASE_URI=' + flaskapp.config['SQLALCHEMY_DATABASE_URI'])


# startup App configuration/setting
# --------------------------------------------------------
if __name__ == '__main__':

    # Load Config
    LoadAppConfiguration(app)
    LoadLoggingConfiguration(app,log)

    # Initialize flask-restplus api
    api.init_app(app)

    # Initialize SQL Alchemy
    db.init_app(app)
    
    # log environment
    LogEnvironment(app, log)

    # Make the WSGI interface available at the top level so wfastcgi can get it.
    wsgi_app = app.wsgi_app
    
    # run di.boards api app
    app.run(host=app.config['HOST'], port = app.config['PORT'])
