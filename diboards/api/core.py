import os
import database
import database.models
import pyqrcode

from flask import current_app as app

# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

# Bulletinboard Logic sector
# --------------------------------------
def create_board(data):

    # Parse data and create Board instance
    board = database.models.Board(
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
    
def read_board(uuid):
    board = database.models.Board.query.filter(Board.uuid == uuid).one()
    return board

def list_boards(user):
    log.info('retrieve board liste by user {}'.format(user.username))
    boardlist = database.models.Board.query.all()
    return boardlist

    
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
    if database.models.User.query.filter_by(username = data.get('username')).first() is not None:
        user = None
        return user
    
    # create user instance
    user = database.models.User(data.get('username'), data.get('password'), data.get('name'))

    # db update
    db.session.add(user)
    db.session.commit()

    return user

def read_user(uuid):
    user = database.models.User.query.filter(User.uuid == uuid).one()
    return user

def list_user(user):
    log.info('retrieve board liste by user {}'.format(user.username))
    userlist = database.models.User.query.all()
    return userlist



# Create Database from scratch
def reset_database():
    db.drop_all()
    db.create_all()

def postmancollection():
    from flask import json
    
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    return json.dumps(data)