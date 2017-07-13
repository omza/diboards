from flask_restplus import fields

# User
# ----------------------------------------------------------------------
#_ = {}
#_['name'] = ''
#_['fields'] = {}


_newuser = {}
_newuser['name'] = 'di.board users sign up'
_newuser['model'] =  {'username': fields.String(required=True, description='email'),
                        'password': fields.String(required=True, description='user password'),
                        'name': fields.String(required=False, description='User name'),
                        #'activationlinkvalidity': fields.Integer(required=False, description='validity of activation link in minutes until creation datetime'),
                        }

_user = {}
_user['name'] = 'di.board users public data'
_user['model'] = {
                    'id': fields.Integer(readOnly=True, required=False, description='The identifier of a user'),
                    #'uuid': fields.String(readOnly=True, required=False, description='The unique identifier of a bulletin board'),
                    'username': fields.String(required=True, description='email'),
                    #'password': fields.String(required=True, description='user password'),
                    'name': fields.String(required=False, description='User name'),
                    #'active': fields.Boolean(required=False, description='user is activated ?'),
                    #'create_date': fields.DateTime(readOnly=True, required=False), 
                    }

_userdetail = {}
_userdetail['name'] = 'di.board user details'
_userdetail['model'] = {
                        'id': fields.Integer(readOnly=True, required=False, description='The identifier of a user'),
                        #'uuid': fields.String(readOnly=True, required=False, description='The unique identifier of a bulletin board'),
                        'username': fields.String(required=True, description='email'),
                        #'password': fields.String(required=True, description='user password'),
                        'name': fields.String(required=False, description='User name'),
                        'active': fields.Boolean(required=False, description='user is activated ?'),
                        #'activationlink': fields.String(readOnly=True, required=False, description='link to activate the user'),
                        #'activationlinkvalidity': fields.Integer(readOnly=True, required=False, description='validity of the activationlink in hours since creation time'),
                        'create_date': fields.DateTime(readOnly=True, required=False), 
                        }

_token = {}
_token['name'] = 'di.board user token'
_token['model'] = {
                    'token': fields.String(readOnly=True, required=True, description='Authentification by token'),
                    'expiration': fields.Integer(readOnly=True, required=False, description='token expires in ... seconds'), 
                    }

""" 
Board 
----------------------------------------------------------------------
"""
_board = {}
_board['name'] = 'Bulletin Board public detail'
_board['model'] = {
                    'id': fields.Integer(readOnly=True, required=False, description='The identifier of a bulletin board'),
                    #'uuid': fields.String(readOnly=True, required=False, description='The unique identifier of a bulletin board'),
                    'name': fields.String(required=True, description='Board name'),
                    'description': fields.String(required=True, description='Board description'),
                    'state': fields.String(required=True, description='Board location state'),
                    'city': fields.String(required=True, description='Board location City'),
                    'zip': fields.String(required=True, description='Board location zip code'),
                    'street': fields.String(required=True, description='Board location street'),
                    'housenumber': fields.String(required=True, description='Board location House Number'),
                    'building': fields.String(required=True, description='Board location Building description'),
    
                    'ownercompany': fields.String(required=True, description='Board owner Company'),
                    'ownercity': fields.String(required=True, description='Board owner City'),
                    'ownerstate': fields.String(required=True, description='Board owner state'),

                    'gpslong': fields.Float(required=False, description='Board location gps longitude'),
                    'gpslat': fields.Float(required=False, description='Board location gps latitude'),
                    'gpsele': fields.Float(required=False, description='Board location gps elevation'),
                    #'gpstime': fields.DateTime(required=False),

                    'active': fields.Boolean(readOnly=True, required=False, description='Board is activated ?'),
                    #'qrcode': fields.String(required=False, description='Link to QR Code'),

                    'create_date': fields.DateTime(readOnly=True, required=False), 
                }

_newboard = {}
_newboard['name'] = 'New Bulletin Board'
_newboard['model'] = {
                    #'id': fields.Integer(readOnly=True, required=False, description='The identifier of a bulletin board'),
                    #'uuid': fields.String(readOnly=True, required=False, description='The unique identifier of a bulletin board'),
                    
                    'name': fields.String(required=True, description='Board name'),
                    'description': fields.String(required=True, description='Board description'),
                    'state': fields.String(required=True, description='Board location state'),
                    'city': fields.String(required=True, description='Board location City'),
                    'zip': fields.String(required=True, description='Board location zip code'),
                    'street': fields.String(required=True, description='Board location street'),
                    'housenumber': fields.String(required=True, description='Board location House Number'),
                    'building': fields.String(required=True, description='Board location Building description'),
                    
                    'gpslong': fields.Float(required=False, description='Board location gps longitude'),
                    'gpslat': fields.Float(required=False, description='Board location gps latitude'),
                    'gpsele': fields.Float(required=False, description='Board location gps elevation'),
                    #'gpstime': fields.DateTime(required=False)
                    
                    #'active': fields.Boolean(readOnly=True, required=False, description='Board is activated ?'),
                    #'qrcode': fields.String(required=False, description='Link to QR Code'),
                    #'create_date': fields.DateTime(readOnly=True, required=False),

                    'allowemail': fields.Boolean(required=True, description='Messenger eMail is allowed ?'),
                    'allowsms': fields.Boolean(required=True, description='Messenger SMS/MMS is allowed ?'),
                    'acceptsubsrequests': fields.Boolean(required=True, description='Should the Board allow subscriptions request from user'),

                    'ownercompany': fields.String(required=True, description='Board owner Company'),
                    'ownerfirstname': fields.String(required=True, description='Board owner first name'),
                    'ownerlastname': fields.String(required=True, description='Board owner last name'),
                    'ownercity': fields.String(required=True, description='Board owner City'),
                    'ownerzip': fields.String(required=True, description='Board owner zip code'),
                    'ownerstreet': fields.String(required=True, description='Board owner street'),
                    'ownerhousenumber': fields.String(required=True, description='Board owner House Number'),
                    'ownerstate': fields.String(required=True, description='Board owner state'),

                }


_boarddetail = {}
_boarddetail['name'] = 'Bulletin Board details'
_boarddetail['model'] = {
                            'id': fields.Integer(readOnly=True, required=False, description='The identifier of a bulletin board'),
                            #'uuid': fields.String(readOnly=True, required=False, description='The unique identifier of a bulletin board'),
                            'name': fields.String(required=True, description='Board name'),
                            'description': fields.String(required=True, description='Board description'),
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

                            'active': fields.Boolean(readOnly=True, required=False, description='Board is activated ?'),
                            #'qrcode': fields.String(required=False, description='Link to QR Code'),

                            'create_date': fields.DateTime(readOnly=True, required=False),

                            'allowemail': fields.Boolean(required=False, description='Messenger eMail is allowed ?'),
                            'allowsms': fields.Boolean(required=False, description='Messenger SMS/MMS is allowed ?'),
                            'acceptsubsrequests': fields.Boolean(required=False, description='Should the Board allow subscriptions request from user'),
                            
                            'ownercompany': fields.String(required=True, description='Board owner Company'),
                            'ownerfirstname': fields.String(required=True, description='Board owner first name'),
                            'ownerlastname': fields.String(required=True, description='Board owner last name'),
                            'ownercity': fields.String(required=True, description='Board owner City'),
                            'ownerzip': fields.String(required=True, description='Board owner zip code'),
                            'ownerstreet': fields.String(required=True, description='Board owner street'),
                            'ownerhousenumber': fields.String(required=True, description='Board owner House Number'),
                            'ownerstate': fields.String(required=True, description='Board owner state'),                            
                        }

_qr = {}
_qr['name'] = 'qrcode'
_qr['model'] = {
                'height': fields.Float(required=True, description='qr code size: height in mm'),
                'width': fields.Float(required=True, description='qr code size: widht in mm'),    
                'roundededges': fields.Boolean(required=False, description='rounded edges'),    
            }
