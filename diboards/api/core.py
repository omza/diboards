import os
from database import db
from database.models import Board, User
from pyqrcode import *
from flask import current_app as app

# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

# Bulletinboard Logic sector
# --------------------------------------
def create_board(data):

    # Parse data and create Board instance
    board = Board(
                  name=data.get('name'), 
                  state=data.get('state'), 
                  city=data.get('city'),
                  zip=data.get('zip'), 
                  street=data.get('street'), 
                  housenumber=data.get('housenumber'), 
                  building=data.get('building'),
                  gpslong = data.get('gpslong'),
                  gpslat = data.get('gpslat'),
                  gpsele = data.get('gpsele'),
                  gpstime = data.get('gpstime'),
                  active=data.get('active'),
                  qrcode = data.get('qrcode')
                  )

    # create qr code an save as png file

    qrpath = app.config['DIBOARDS_PATH_QR'] + board.uuid
    log.info(qrpath)
    if not os.path.exists(qrpath):
        os.makedirs(qrpath)
        os.chmod(qrpath, 0o755)

    qrfile = qrpath + '/qr-' + board.uuid + '.png'
    log.info(qrfile)

    qrlink = qrfile
    log.info(qrlink)

    url = pyqrcode.create(qrlink)
    url.png(qrfile, scale=10, module_color=(255, 45, 139, 255), background=(255, 255, 255, 255), quiet_zone=4)
    board.qrcode = qrlink

    # db update
    db.session.add(board)
    db.session.commit()

    return board

def update_board(uuid, data):
    category = Category.query.filter(Category.id == category_id).one()
    category.name = data.get('name')
    db.session.add(category)
    db.session.commit()

def delete_board(uuid):
    category = Category.query.filter(Category.id == category_id).one()
    db.session.delete(category)
    db.session.commit()
    
    
# User Logic sector
# ----------------------------------------
def delete_user(uuid):
    category = Category.query.filter(Category.id == category_id).one()
    db.session.delete(category)
    db.session.commit()
    pass

def update_user(uuid, data):
    category = Category.query.filter(Category.id == category_id).one()
    category.name = data.get('name')
    db.session.add(category)
    db.session.commit()

def create_user(data):
    
    # user already exist ?
    if User.query.filter_by(username = data.get('username')).first() is not None:
        user = None
        return user
    
    # create user instance
    user = User(data.get('username'), data.get('password'), data.get('name'))

    # db update
    db.session.add(user)
    db.session.commit()

    return user

# Create Database from scratch
def reset_database():
    db.drop_all()
    db.create_all()