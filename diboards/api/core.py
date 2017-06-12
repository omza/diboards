# imports & globals
# -----------------------------------------------------

import os

from database import db
from datetime import datetime, timedelta

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
    board = database.models.Board.query.filter(database.models.Board.uuid == uuid).one()
    return board

def list_boards(params = None):

    # concat filters
    boardsfilter = ''
    for key, value in params.items():
        if key == 'id':
            try:
                id = int(value)
                if id > 0:
                    boardsfilter = boardsfilter + '(board.id == ' + str(id) + ') and '
                elif id < 0:
                    return 403, None
            except:
                return 403, None
    boardsfilter = boardsfilter[:-5]       
    log.info('retrieve board liste with filters {!s}'.format(boardsfilter)) 

    # retrieve boardlist
    boardlist = database.models.Board.query.filter(boardsfilter).all()
    if boardlist is None:
        return 404, None

    return 200, boardlist


# QRCODES Logic sector

def create_qrcode(uuid, data, authuser):
    
    #retrieve board
    board = database.models.Board.query.filter(database.models.Board.uuid == uuid).one()
    if board is None:
        return 404, None
    
    # check rights: 
    # Only Board Owner can retrieve a QR code  
    if authuser.uuid == '':
        return 403, None
    
    #retrieve request data
    height = data.get('height')
    width = data.get('width')
    roundededges = data.get('roundededges')
    
    # create qr code an save as png file
    qrpath = app.config['DIBOARDS_PATH_QR'] + uuid
    if not os.path.exists(qrpath):
        os.makedirs(qrpath)
        os.chmod(qrpath, 0o755)

    qrpath = qrpath + '/'
    qrfile = 'qr-' + board.uuid + '.png'
    qrfull = qrpath + qrfile

    url = pyqrcode.create(qrfull)
    url.png(qrfull, scale=10, module_color=(255, 45, 139, 255), background=(255, 255, 255, 255), quiet_zone=4)

    log.debug(qrpath + qrfile)
    
    return 200, qrfile, qrpath


    
# User Logic sector
# ----------------------------------------
def delete_user(AuthUser):
    
    # Check authorized in user
    if AuthUser is None:
        return 401
    
    AuthUser.active = False

    # delete user
    db.session.add(AuthUser)
    db.session.commit()

    return 200


def update_user(id, data):
    user = database.models.User.query.filter(database.models.User.id == id).one()
    
    if user is None:
        return 404

    for key, value in data.items():
        if key == 'name':
            user.name = value
        elif key == 'active':
            user.active = value
        elif key == 'password':
            user.hash_password(value)

    db.session.add(user)
    db.session.commit()
    return 200

def activate_user(id,email):

    # retrieve user
    user = database.models.User.query.filter(database.models.User.id == id).one()

    if user is None:
        return 404
    
    #parametercheck successfull/ activationlink correct ?
    if user.username != email:
        return 403

    #check validity (duration of link)
    if (user.active) or (not user.verify_activationvalidity()):
        return 408

    # db update
    user.active = True
    user.activationlink = ''
    user.activationlinkvalidity = 0

    db.session.add(user)
    db.session.commit()
    return 200
    
def create_user(data):
    
    # user already exist ?
    if database.models.User.query.filter_by(username = data.get('username')).first() is not None:
        return 403, None
    
    # create user instance
    user = database.models.User(data.get('username'), data.get('password'), data.get('name'), False, data.get('activationlinkvalidity'))
    
    # user
    if not user.verify_emailadress():
        return 400, None

    # db update
    db.session.add(user)
    db.session.commit()

    return 200, user

def select_user(AuthUser):
    
    # Check authorized in user
    if AuthUser is None:
        return 401, None
        
    # Check User Scope
    log.debug('USER: ' + AuthUser.username)
    user = database.models.User.query.filter(database.models.User.uuid == AuthUser.uuid).one()
    
    if user is None:
        return 404, None
    else:
        return 200, user
        

def list_user(user):
    log.info('retrieve board liste by user {}'.format(user.username))
    userlist = database.models.User.query.all()
    return userlist



# Create Database from scratch
def reset_database():
    log.warning('try to create db from scratch')
    db.drop_all()
    db.create_all()

def postmancollection():
    from flask import json
    
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    return json.dumps(data)