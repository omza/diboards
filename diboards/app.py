# Import
import os
from flask import Flask
from api import api
from core import db

# Flask app instance
app = Flask(__name__, instance_relative_config=True)

def appconfig(flaskapp):
    # Load the default configuration
    flaskapp.config.from_object('config.default')
 
    # Load the configuration from the instance folder
    flaskapp.config.from_pyfile('secrets.py')
 
    # Load the file specified by the APP_CONFIG_FILE environment variable
    # Variables defined here will override those in the default configuration
    flaskapp.config.from_envvar('APP_CONFIG_FILE')


def printenvironment(flaskapp):
    
    print('-')
    if app.config['SERVER_NAME'] is not None:
        print('SERVER_NAME=' + app.config['SERVER_NAME'])
    else:
        print('SERVER_NAME=none')
    
    print('HOST=' + app.config['HOST'])
    print('PORT=' + str(app.config['PORT']))
    print('DEBUG=' + str(app.config['DEBUG']))
    
    print('APP_CONFIG_FILE=' + os.environ.get('APP_CONFIG_FILE','No APP Config file'))

    print('SQLALCHEMY_DATABASE_URI=' + app.config['SQLALCHEMY_DATABASE_URI'])
    print('-')

# startup App configuration/setting
if __name__ == '__main__':
    
    # load settings
    appconfig(app)

    # Initialize flask-restplus api
    api.init_app(app)

    # Initialize SQL Alchemy
    db.init_app(app)
    
    #printenvironment
    if app.config['DEBUG']:
           printenvironment(app)
    else:
        print('no debug environment')

    # Make the WSGI interface available at the top level so wfastcgi can get it.
    wsgi_app = app.wsgi_app
    
    # run di.boards api app
    app.run(host=app.config['HOST'], port = app.config['PORT'])
