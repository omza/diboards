from database import db
from datetime import datetime, timedelta
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from flask import current_app as app
import uuid
import re

# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

""" subscription db model
    -------------------------------------------------------------------------
"""
class Subscription(db.Model):
    __tablename__ = 'subscription'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), primary_key = True)
    
    role = db.Column(db.String(10))
    flow = db.Column(db.String(10))
    flowstatus = db.Column(db.String(10))
    active = db.Column(db.Boolean)
    create_date = db.Column(db.DateTime)

    user = db.relationship('User', back_populates="boards")
    board = db.relationship('Board', back_populates="users")


""" Board db model
   -------------------------------------------------------------------------
"""
class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(32), index=True)
    
    name = db.Column(db.String(50))
    description = db.Column(db.String(100))

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
    
    """ bord settings allowed messengers """
    allowemail = db.Column(db.Boolean)
    allowsms = db.Column(db.Boolean)

    """ bord settings allowed workflows """
    acceptsubsrequests  = db.Column(db.Boolean)

    """ board owner """
    ownercompany = db.Column(db.String(100))    
    ownerlastname = db.Column(db.String(50))
    ownerfirstname = db.Column(db.String(50))
    ownerstate = db.Column(db.String(50))
    ownercity = db.Column(db.String(50))
    ownerzip = db.Column(db.String(5))
    ownerstreet = db.Column(db.String(50))
    ownerhousenumber = db.Column(db.String(10))
    
    users = db.relationship("Subscription", back_populates="board")
    qrcodes = db.relationship("QRcode", back_populates="board") 

    def __init__(self, data):
        
        """ auto keys """
        self.active = True
        self.uuid = str(uuid.uuid4())
        self.create_date = datetime.utcnow()
        
        log.info('A new Board raises with uuid {}'.format(self.uuid))

        """ parse and log data dictionary into instance var """
        for key, value in data.items():
            if (not key in vars(self)) and (key in vars(Board)):
                setattr(self, key, value)
            
        for key, value in vars(self).items():   
            log.info('Board {} - member: {} = {!s}'.format(self.uuid,key,value))
               
""" user db model
   -------------------------------------------------------------------------
"""
class User(db.Model):
    __tablename__ = 'user'
    _emailverificationre = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

    id = db.Column(db.Integer, primary_key = True)
    uuid = db.Column(db.String(32), index=True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean)
    name = db.Column(db.String(32))
    create_date = db.Column(db.DateTime)
    #activationlink = db.Column(db.String(128))
    activationvalidity = db.Column(db.DateTime)
    termsofservicelink = db.Column(db.String(128))
    termsofserviceaccepted = db.Column(db.DateTime)
    pwresetquestion = db.Column(db.String(32))
    pwresetanswer_hash = db.Column(db.String(128))

    boards = db.relationship("Subscription", back_populates="user")
    
    # methods
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
        
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def hash_pwresetanswer(self, pwresetanswer):
        self.pwresetanswer_hash = pwd_context.encrypt(pwresetanswer)
    
    """ check secret answer to pw reset question """
    def verify_pwresetanswer(self, pwresetanswer = None):
        
        if (pwresetanswer is None) or (pwresetanswer == ''):
            returnvalue = False
        else:
            returnvalue = pwd_context.verify(pwresetanswer, self.pwresetanswer_hash)

        return returnvalue

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
        log.info('validate username {} with regex {} : {!s}'.format(self.username, User._emailverificationre, dummy))

        if dummy is None:
            return False
        else:
            return True
        pass

    """ activation valid (in timeframe)? """
    def verify_activationvalidity(self):     
        if (datetime.utcnow() <= self.activationvalidity):
            return True
        else:
            return False

    """ constructor """
    def __init__(self, data):

        """ auto keys """
        self.active = False
        self.uuid = str(uuid.uuid4())
        self.create_date = datetime.utcnow()
        self.termsofservicelink = app.config['DIBOARDS_PATH_TERMSOFSERVICE']

        log.info('A new User raises with uuid {}'.format(self.uuid))

        """ parse and log data dictionary into instance var """
        for key, value in data.items():

            if key == 'password':
                self.hash_password(value)
            elif key == 'pwresetanswer':
                self.hash_pwresetanswer(value)
            elif key == 'activationvalidity':
                self.activationvalidity = self.create_date + timedelta(hours=value)
            elif (not key in vars(self)) and (key in vars(User)):
                setattr(self, key, value)
            
        for key, value in vars(self).items():   
            log.info('User {} - member: {} = {!s}'.format(self.uuid,key,value))

""" qr db model
   -------------------------------------------------------------------------
"""        
class QRcode(db.Model):
    __tablename__ = 'qrcodes'
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), primary_key = True)
    
    height = db.Column(db.Integer, primary_key = True)
    width = db.Column(db.Integer, primary_key = True)
    roundedges = db.Column(db.Boolean, primary_key = True)
    file = db.Column(db.String(50))
    
    create_date = db.Column(db.DateTime)

    board = db.relationship('Board', back_populates="qrcodes")




