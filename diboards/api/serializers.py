from flask_restplus import fields
from api import api

# User
# ----------------------------------------------------------------------

newuser = api.model('di.board users sign up', {
    'username': fields.String(required=True, description='email'),
    'password': fields.String(required=True, description='user password'),
    'name': fields.String(required=False, description='User name'),
    'activationlinkvalidity': fields.Integer(required=False, description='validity of activation link in minutes until creation datetime'),
})

user = api.model('di.board users public data', {
    #'id': fields.Integer(readOnly=True, required=False, description='The identifier of a user'),
    'uuid': fields.String(readOnly=True, required=False, description='The unique identifier of a bulletin board'),
    'username': fields.String(required=True, description='email'),
    #'password': fields.String(required=True, description='user password'),
    'name': fields.String(required=False, description='User name'),
    #'active': fields.Boolean(required=False, description='user is activated ?'),
    #'create_date': fields.DateTime(readOnly=True, required=False), 
})

userdetail = api.model('di.board user details', {
    'id': fields.Integer(readOnly=True, required=False, description='The identifier of a user'),
    'uuid': fields.String(readOnly=True, required=False, description='The unique identifier of a bulletin board'),
    'username': fields.String(required=True, description='email'),
    #'password': fields.String(required=True, description='user password'),
    'name': fields.String(required=False, description='User name'),
    'active': fields.Boolean(required=False, description='user is activated ?'),
    'activationlink': fields.String(readOnly=True, required=False, description='link to activate the user'),
    'activationlinkvalidity': fields.Integer(readOnly=True, required=False, description='validity of the activationlink in hours since creation time'),
    'create_date': fields.DateTime(readOnly=True, required=False), 
})

token = api.model('di.board user token', {
    'token': fields.String(readOnly=True, required=True, description='Authentification by token'),
    'validuntil': fields.DateTime(readOnly=True, required=False, description='token is valid until'), 
})



# Board 
# ----------------------------------------------------------------------
board = api.model('Bulletin Board public detail', {
    #'id': fields.Integer(readOnly=True, required=False, description='The identifier of a bulletin board'),
    'uuid': fields.String(readOnly=True, required=False, description='The unique identifier of a bulletin board'),
    'name': fields.String(required=True, description='Board name'),
    'state': fields.String(required=True, description='Board location state'),
    'city': fields.String(required=True, description='Board location City'),
    'zip': fields.String(required=True, description='Board location zip code'),
    'street': fields.String(required=True, description='Board location street'),
    'housenumber': fields.String(required=True, description='Board location House Number'),
    'building': fields.String(required=True, description='Board location Building description'),
    
    #'gpslong': fields.Float(required=False, description='Board location gps longitude'),
    #'gpslat': fields.Float(required=False, description='Board location gps latitude'),
    #'gpsele': fields.Float(required=False, description='Board location gps elevation'),
    #'gpstime': fields.DateTime(readOnly=True, required=False),

    'active': fields.Boolean(readOnly=True, required=True, description='Board is activated ?'),
    #'qrcode': fields.String(required=False, description='Link to QR Code'),

    #'create_date': fields.DateTime(readOnly=True, required=False), 
})

boarddetail = api.model('Bulletin Board details', {
    'id': fields.Integer(readOnly=True, required=False, description='The identifier of a bulletin board'),
    'uuid': fields.String(readOnly=True, required=False, description='The unique identifier of a bulletin board'),
    'name': fields.String(required=True, description='Board name'),
    'state': fields.String(required=True, description='Board location state'),
    'city': fields.String(required=True, description='Board location City'),
    'zip': fields.String(required=True, description='Board location zip code'),
    'street': fields.String(required=True, description='Board location street'),
    'housenumber': fields.String(required=True, description='Board location House Number'),
    'building': fields.String(required=True, description='Board location Building description'),
    
    'gpslong': fields.Float(required=False, description='Board location gps longitude'),
    'gpslat': fields.Float(required=False, description='Board location gps latitude'),
    'gpsele': fields.Float(required=False, description='Board location gps elevation'),
    'gpstime': fields.DateTime(readOnly=True, required=False),

    'active': fields.Boolean(readOnly=True, required=True, description='Board is activated ?'),
    #'qrcode': fields.String(required=False, description='Link to QR Code'),

    'create_date': fields.DateTime(readOnly=True, required=False), 
})

qr = api.model('qrcode', {
    'height': fields.Float(required=True, description='qr code size: height in mm'),
    'width': fields.Float(required=True, description='qr code size: widht in mm'),    
    'roundededges': fields.Boolean(required=False, description='rounded edges'),    
})