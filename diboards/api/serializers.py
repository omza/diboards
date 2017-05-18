from flask_restplus import fields
from api import api

# User
# ----------------------------------------------------------------------
user = api.model('di.board users', {
    #'id': fields.Integer(readOnly=True, required=False, description='The identifier of a user'),
    'uuid': fields.String(readOnly=True, required=False, description='The unique identifier of a bulletin board'),
    'username': fields.String(required=True, description='email'),
    #'password': fields.String(required=True, description='user password', attribute='password_hash'),
    'name': fields.String(required=False, description='User name'),
    'active': fields.Boolean(required=False, description='user is activated ?'),
    #'create_date': fields.DateTime(readOnly=True, required=False), 
})

newuser = api.model('di.board users sign up', {
    'username': fields.String(required=True, description='email'),
    'password': fields.String(required=True, description='user password'),
    'name': fields.String(required=False, description='User name'),
})

token = api.model('di.board user token', {
    'token': fields.String(readOnly=True, required=True, description='Authentification by token'),
})



# Board 
# ----------------------------------------------------------------------
board = api.model('Bulletin Board', {
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