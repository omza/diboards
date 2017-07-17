from flask import request, g, current_app as app
from flask_restplus import Namespace, Resource, fields
from auth import basicauth
from database import db
from database.models import User, Board, Subscription

import os
from datetime import datetime, timedelta
import pyqrcode

""" logger """
import logging
log = logging.getLogger('diboardapi.' + __name__)

""" namespaces """
api = Namespace('user', description='user related operations')


""" Register Models ----------------------------------------------------------------------------------------------

        user_public = api.model(_user['name'], _user['model'])
        user_new = api.model(_newuser['name'], _newuser['model'])
        user_detail = api.model(_userdetail['name'], _userdetail['model'])
        user_update = api.model(_userupdate['name'], _userupdate['model']) 
        user_token = api.model(_token['name'], _token['model'])
        board_public = api.model(_board['name'], _board['model']

"""

user_new = api.model('di.board users sign up', {'username': fields.String(required=True, description='email'),
                                                'password': fields.String(required=True, description='user password'),
                                                'name': fields.String(required=False, description='User name'),
                                                })

user_detail = api.model('di.board user details', {'id': fields.Integer(readOnly=True, required=False, description='The identifier of a user'),
                                                    #'uuid': fields.String(readOnly=True, required=False, description='The unique identifier of a bulletin board'),
                                                    'username': fields.String(required=True, description='email'),
                                                    'name': fields.String(required=False, description='User name'),
                                                    'active': fields.Boolean(required=False, description='user is activated ?'),
                                                    'create_date': fields.DateTime(readOnly=True, required=False), 
                                                    })

user_update = api.model('di.board users update', {'password': fields.String(required=False, description='user password'),
                                                    'name': fields.String(required=False, description='User name'),
                                                    'active': fields.Boolean(required=False, description='user is activated ?')
                                                    })

user_token = api.model('di.board user token', {'token': fields.String(readOnly=True, required=True, description='Authentification by token'),
                                                'expiration': fields.Integer(readOnly=True, required=False, description='token expires in ... seconds'), 
                                                })

user_subscriptions = api.model('Bulletin Board public detail', {
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
                    'gpstime': fields.DateTime(required=False, description='Board location gps elevation'),

                    'create_date': fields.DateTime(readOnly=True, required=False), 
                })
        


""" Endpoints ---------------------------------------------------------------------------------------------------   

        /user
        /user/activate
        /user/token
        /user/subscription

"""

@api.route('/')
class UserInstance(Resource):
    
    """ swagger responses as class variables """
    _responses = {}
    _responses['get'] = {   
                            200: ('Success', user_detail),
                            401: 'Missing Authentification or wrong credentials',
                            403: 'Insufficient rights e.g. User ist not activated'
                        }
    _responses['post'] = {200: ('User signed successfully up.', user_detail),
                          400: 'not a valid email address',
                          403: 'User already signed up'
                         }
    _responses['delete'] = {200: 'User is deactivated now',
                    401: 'Missing Authentification or wrong credentials',
                    403: 'Insufficient rights e.g. User is not activated or deleted'
                }

    """ select userdetails """
    @api.doc(description='select/read user detail', security='basicauth', responses = _responses['get'])
    @basicauth.login_required
    @api.marshal_with(user_detail)
    def get(self):        
        
        """ parse request """
        AuthUser = g.get('user')
        if AuthUser is None:
             api.abort(401, __class__._responses['post'][401])
        
        """ logging """
        log.info('get_user: {!s}'.format(AuthUser.id))
        
        """ User Active ? """
        if AuthUser.active == False:
            api.abort(403, __class__._responses['get'][403]) 
        
        """ return AuthUser details """
        return AuthUser, 200
    

    """ update user """
    @api.doc(description='update user', security='basicauth', responses = _responses['get'])
    @api.expect(user_update)
    @api.marshal_with(user_detail)
    @basicauth.login_required    
    def put(self):                       

        """ parse request """
        AuthUser = g.get('user')
        if AuthUser is None:
             api.abort(401, __class__._responses['get'][401])
        data = request.json

        """ logging """
        log.info('update user: {!s}'.format(AuthUser.id))

        """ User Active ? """
        if AuthUser.active == False:
            api.abort(403, __class__._responses['get'][403])  

        """ update all fields """
        for key, value in data.items():
            log.debug('update user (key == value): {!s} == {!s}'.format(key, value))
            if key == 'password':
                AuthUser.hash_password(value)
            else:
                if (key in vars(AuthUser)):
                    setattr(AuthUser, key, value)
 
        """ db update """
        log.debug('update db')
        db.session.add(AuthUser)
        db.session.commit()

        return AuthUser, 200
        
    """ delete user """
    @api.doc(description='delete an user', security='basicauth', responses = _responses['delete'])
    @basicauth.login_required
    def delete(self):
                
        """ parse request """
        AuthUser = g.get('user')
        if AuthUser is None:
             api.abort(401, __class__._responses['post'][401])
        
        """ logging """
        log.info('delete user: {!s}'.format(AuthUser.id))
        
        """ check active user """
        if (not AuthUser.active):
            api.abort(403, __class__._responses['delete'][403])
        
        """ delete user """
        AuthUser.active = False

        db.session.add(AuthUser)
        db.session.commit()

        return 200       
              
    """ create user """
    @api.doc(description='create a new user', responses = _responses['post'])
    @api.expect(user_new)
    @api.marshal_with(user_detail)
    def post(self):
        
        """ parse request """      
        data = request.json
        email = data.get('username')
        password = data.get('password')
        name = data.get('name')

        """ logging """
        log.info('create user: {!s}{!s}'.format(email, name))
        
        """ user already exists ? """
        if (User.query.filter_by(username = email).first() is not None):
            api.abort(403, __class__._responses['post'][403])

        """ create user instance """
        diboarduser = User(email,password, name)

        """ email adress not valid ? """
        if not diboarduser.verify_emailadress():
            api.abort(httpstatus, __class__._responses['post'][httpstatus])
        
        """ db update """
        db.session.add(diboarduser)
        db.session.commit()

        return diboarduser, 200

   
@api.route('/activate')
@api.param(name = 'id', description = 'The unique identifier of a di.board user',type = int, required=True)
@api.param(name='email', description='emailaddress to activate', type=str, required=True)
class Activate(Resource):

    # response codes
    _responses = {200: 'User activated', 
                  403: 'Insufficient rights or bad link', 
                  404: 'User not found', 
                  408: 'activation link is not valid anymore or user is already activated'
                  }

    @api.doc(description='activate a diboard user', responses=_responses)
    def get(self):
        
        # parse request args       
        try:
            id = request.args.get('id',default=0, type=int)
            email = request.args.get('email',default='', type=str)
        except ValueError:
            id = 0
            email = ''
        
        log.info('activate id:{!s} and email:{}'.format(id,email))

        """ retrieve user """
        diboarduser = User.query.get(id)
        if (diboarduser is None):
            api.abort(404, __class__._responses[404])

        """ already activated ? """
        if (diboarduser.active):
            api.abort(408, __class__._responses[408])

        """ activate user and db update """
        diboarduser.active = True
        db.session.add(diboarduser)
        db.session.commit()

        return 200
        
@api.route('/token')
@api.param(name = 'expiration', description = 'access token validity in seconds (default 10 min.)', type = int)
class Token(Resource):
    
    # response codes
    _responses = {200: ('token successfully generated', user_token),
                  401: 'Missing Authentification or wrong credentials',
                  403: 'Insufficient rights e.g. User ist not activated'
                 }
    
    @api.doc(description='get_user_token', security='basicauth', responses=_responses)
    @basicauth.login_required
    @api.marshal_with(user_token)
    def get(self):
        
        """ parse request """
        AuthUser = g.get('user')
        if AuthUser is None:
             api.abort(401, __class__._responses[401])

        try:
            expiration = request.args.get('expiration',default=600, type=int)
        except ValueError:
            expiration = 600

        """ User Active ? """
        if AuthUser.active == False:
            api.abort(403, __class__._responses[403]) 

        # generate token
        token = AuthUser.generate_auth_token(expiration)
        token = token.decode('ascii')
        log.debug('token {} expires in {} seconds'.format(str(token),str(expiration)))

        # prepare return
        diboardstoken = {'token' : token, 'expiration': expiration}
        return diboardstoken, 200


@api.route('/subscriptions')
class Subscriptions(Resource):
    
    # swagger responses   
    _responses = {200: ('Success', user_subscriptions),
                  401: 'Missing Authentification or wrong credentials',
                  403: 'Insufficient rights',
                  404: 'No Subscriptions found'
                  }
    
    @api.doc(description='retrieve a list of boards the user is subscribed', security='basicauth', responses=_responses)
    @basicauth.login_required
    @api.marshal_with(user_subscriptions)
    def get(self):

        # retrieve boardlist
        #httpstatus, diboards = list_boards(g.user)

        # return httpstatus, object
        if httpstatus in __class__._responses:
            if httpstatus == 200:
                return diboards, 200
            else:
                api.abort(httpstatus, __class__._responses[httpstatus])
        else:
            api.abort(500)
