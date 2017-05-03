"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

#
import os
from flask import Flask
from api import api
from core import db


app = Flask(__name__, instance_relative_config=True)


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

    # Make the WSGI interface available at the top level so wfastcgi can get it.
    wsgi_app = app.wsgi_app
    
    # run di.boards api app
    print('HOST=' + app.config['HOST'])
    print('PORT=' + str(app.config['PORT']))
    print('DEBUG=' + str(app.config['DEBUG']))
    app.run(host=app.config['HOST'], port = app.config['PORT'], debug=app.config['DEBUG'])
