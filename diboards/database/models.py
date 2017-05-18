from database import db
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from flask import current_app as app
import uuid
import re

# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

# board db model
# ----------------------------------------------------------------------------

class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), index=True)
    
    name = db.Column(db.String(50))

    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    zip = db.Column(db.String(5))
    street = db.Column(db.String(50))
    housenumber = db.Column(db.String(10))
    building = db.Column(db.String(20))
    
    gpslong = db.Column(db.Float)
    gpslat = db.Column(db.Float)
    gpsele = db.Column(db.Float)
    gpstime = db.Column(db.DateTime)

    active = db.Column(db.Boolean)
    qrcode = db.Column(db.String(100))
    
    create_date = db.Column(db.DateTime)
    
    users = db.relationship("Subscription", back_populates="board")
    
    def __init__(self, name, state, city, zip, street, housenumber, building, gpslong=None, gpslat=None, gpsele=None, gpstime=None, active=False, qrcode=None):
        
        self.uuid = str(uuid.uuid4())

        self.name = name
         
        self.state = state
        self.city = city
        self.zip = zip
        self.street = street
        self.housenumber = housenumber
        self.building = building

        self.gpslong = gpslong
        self.gpslat = gpslat
        self.gpsele = gpsele
        #self.gpstime = gpstime

        self.active = active
        self.qrcode = qrcode

        self.create_date = datetime.utcnow()

        log.info('A new Board #{} raises with uuid {}'.format(self.id, self.uuid))

    def __repr__(self):
        return '<Board %r>' % self.name


# user db model
# -------------------------------------------------------------------------

class User(db.Model):
    __tablename__ = 'users'
    _emailverificationre = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

    id = db.Column(db.Integer, primary_key = True)
    uuid = db.Column(db.String(32), index=True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean)
    name = db.Column(db.String(32))
    create_date = db.Column(db.DateTime)
    boards = db.relationship("Subscription", back_populates="user")
    
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
        

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

    def verify_emailadress(self):

        dummy = re.match(User._emailverificationre,self.username)
        log.debug('validate username {} with regex {} : {!s}'.format(self.username, User._emailverificationre, dummy))

        if dummy is None:
            return False
        else:
            return True
        pass

    def __init__(self, username, password, name='', active = False):
        self.uuid = str(uuid.uuid4())
        self.create_date = datetime.utcnow()
        
        self.username = username
        self.hash_password(password)

        self.name = name
        self.active = active

    def __repr__(self):
        return '<User %r>' % self.username

# subscription db model
# -------------------------------------------------------------------------
class Subscription(db.Model):
    __tablename__ = 'subscription'
    userid = db.Column(db.Integer, db.ForeignKey('board.id') ,primary_key = True)
    boardid = db.Column(db.Integer, db.ForeignKey('users.id') ,primary_key = True)
    roleid = db.Column(db.String(10))
    flowid = db.Column(db.String(10))
    flowstatus = db.Column(db.String(10))
    active = db.Column(db.Boolean)
    create_date = db.Column(db.DateTime)
    user = db.relationship('User', back_populates="boards")
    board = db.relationship('Board',back_populates="users")


    def __init__(self, userid, boardid, roleid, flowid):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

