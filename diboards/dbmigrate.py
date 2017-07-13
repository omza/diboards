import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


""" Initialize and Config Flask app """
app = Flask(__name__)   

app.config.from_object('config.default')
app.config.from_envvar('DIBOARDS_CONFIG_FILE')
if os.path.isfile('/secrets/secrets.py'):
    app.config.from_pyfile('/secrets/secrets.py', silent=True)
else:
    app.config.from_object('config.secrets')

""" import models and db """
from database import db 
from database.models import Board, Subscription, User
db.init_app(app)


""" Init Flask - Migrate and Script """
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()