from flask import request, g, current_app as app, json
from flask_restplus import Namespace, Resource, fields
from auth import basicauth
from database import db
from database.models import User, Board, Subscription

import os, random, string
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

user_new = api.model('di.board users sign up', {'username': fields.String(required=True, description='email == username'),
                                                'password': fields.String(required=True, description='user password'),
                                                'name': fields.String(required=False, description='User name'),
                                                'pwresetquestion': fields.String(required=True, description='question for password reset'),
                                                'pwresetanswer': fields.String(required=True, description='secret answer for password reset'),
                                                'activationvalidity': fields.Integer(required=False, description='validity of activation link (in hours)'),
                                                })

user_detail = api.model('di.board user details', {'id': fields.Integer(readOnly=True, required=False, description='The identifier of a user'),
                                                    #'uuid': fields.String(readOnly=True, required=False, description='The unique identifier of a bulletin board'),
                                                    'username': fields.String(required=True, description='email'),
                                                    'name': fields.String(required=False, description='User name'),
                                                    'termsofservicelink': fields.String(readOnly=True,required=False, description='link to terms of services'),
                                                    'termsofserviceaccepted': fields.DateTime(readOnly=True, required=False, description='date user has accepted terms of service'),
                                                    'active': fields.Boolean(required=False, description='user is activated ?'),
                                                    'create_date': fields.DateTime(readOnly=True, required=False), 
                                                    })

user_update = api.model('di.board users update', {'password': fields.String(required=False, description='user password'),
                                                    'name': fields.String(required=False, description='User name'),
                                                    #'active': fields.Boolean(required=False, description='user is activated ?')
                                                    })

user_token = api.model('di.board user token', {'token': fields.String(readOnly=True, required=True, description='Authentification by token'),
                                                'expiration': fields.Integer(readOnly=True, required=False, description='token expires in ... seconds'), 
                                                })

board_public = api.model('Bulletin Board public detail', {
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
    #'gpstime': fields.DateTime(required=False, description='Board location gps elevation'),
    'create_date': fields.DateTime(readOnly=True, required=False)})

subscription = api.model('Users Subscription', {
    #'userid': fields.Integer(readOnly=True, required=False, description='The identifier of a user'),
    #'boardid': fields.Integer(readOnly=True, required=False, description='The identifier of a user'),
    'role': fields.String(readOnly=True, required=True, description='subscription role'),
    'flow': fields.String(readOnly=True, required=True, description='subscription process'),
    'flowstatus': fields.String(readOnly=True, required=True, description='subscription process status'),
    'create_date': fields.DateTime(readOnly=True, required=True),
    'board': fields.Nested(model=board_public, as_list=True)})

user_subscriptions = user_detail.clone('Bulletin Board public detail', {
    'subscriptions': fields.Nested(attribute='boards',model=subscription,as_list=True)})

user_pwreset = api.model('di.board password reset question', {
    'id': fields.Integer(readOnly=True, required=True, description='The identifier of a user'),
    'username': fields.String(readOnly=True,required=True, description='email == username'),
    'pwresetquestion': fields.String(readOnly=True, required=True, description='question for password reset')})

user_new_pw = api.model('di.board new password (reset)', {
    'id': fields.Integer(readOnly=True, required=True, description='The identifier of a user'),
    'username': fields.String(readOnly=True,required=True, description='email == username'),
    'password': fields.String(readOnly=True, required=True, description='new password after password reset')})

""" Endpoints ---------------------------------------------------------------------------------------------------   
        /user
        /user/activate
        /user/token
        /user/subscription
        /user/pwreset

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
        
        """ show user all its data """
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
    @api.doc(description='user can update their own data and settings', security='basicauth', responses = _responses['get'])
    @api.expect(user_update)
    @api.marshal_with(user_detail)
    @basicauth.login_required    
    def put(self):                       

        """ user update own data """
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
    

    @api.doc(description='delete an user', security='basicauth', responses = _responses['delete'])
    @basicauth.login_required
    def delete(self):
                
        """ deactivate the authorized user """
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
        
        """ user sign up """      
        data = request.json
        email = data.get('username')
        password = data.get('password')
        name = data.get('name')
        activationvalidity = data.get('activationvalidity')

        """ logging """
        log.info('create user: {!s}{!s}'.format(email, name))
        
        """ user already exists ? """
        if (User.query.filter_by(username = email).first() is not None):
            api.abort(403, __class__._responses['post'][403])

        """ create user instance """
        diboarduser = User(data)

        """ email adress not valid ? """
        if not diboarduser.verify_emailadress():
            api.abort(400, __class__._responses['post'][400])
        
        """ db update """
        db.session.add(diboarduser)
        db.session.commit()

        return diboarduser, 200

   
@api.route('/activate')
@api.param(name = 'id', description = 'The unique identifier of a di.board user',type = int, required=True)
@api.param(name='email', description='emailaddress to activate', type=str, required=True)
@api.param(name='termsofserviceaccepted', description='does user accept known terms of service', type=bool, required=True)
class Activate(Resource):

    # response codes
    _responses = {200: 'User activated', 
                  403: 'Insufficient rights, user has not accepted terms of service or bad link', 
                  404: 'User not found', 
                  408: 'activation link is not valid anymore or user is already activated'
                  }

    @api.doc(description='activate a diboard user', responses=_responses)
    def get(self):
        
        """ activate user / confirm by id and username/email """       
        try:
            id = request.args.get('id',default=0, type=int)
            email = request.args.get('email',default='', type=str)
            termsofserviceaccepted = request.args.get('termsofserviceaccepted',default=False, type=bool)
        except ValueError:
            id = 0
            email = ''
            termsofserviceaccepted  = False
        
        log.info('activate id:{!s} and email:{}'.format(id,email))

        """ terms of service accepted ? """
        if not termsofserviceaccepted:
            api.abort(403, __class__._responses[403])

        """ retrieve user """
        diboarduser = User.query.get(id)
        if (diboarduser is None):
            api.abort(404, __class__._responses[404])

        """ doublecheck with eMail """
        if (diboarduser.username != email):
            api.abort(403, __class__._responses[403])

        """ already activated or link is not valid anymore? """
        if (diboarduser.active) or (not diboarduser.verify_activationvalidity):
            api.abort(408, __class__._responses[408])

        """ activate user and db update """
        diboarduser.active = True
        diboarduser.termsofserviceaccepted = datetime.utcnow()

        db.session.add(diboarduser)
        db.session.commit()

        return 200


"""
    Password reset with secret answer (pwresetanswer_hash) to a pw reset question (pwresetquestion)
    
    /pwreset [GET] send user id an pw reset question in the response body. Need user id or email/account
    /pwreset [POST] reset the user password and send the new one in the response body. Need user id or email/account AND the secret answer (pwresetanswer_hash)
   
"""
@api.route('/pwreset')
@api.param(name='id', description='The unique identifier of a di.board user',type=int, required=False)
@api.param(name='email', description='emailaddress/ account', type=str, required=False)
@api.param(name='pwresetanswer', description='does user accept known terms of service', type=str, required=False)
class PwReset(Resource):

    # response codes
    _responses = {}
    _responses['get'] = {
                        200: ('Success', user_pwreset),
                        403: 'Insufficient rights e.g. User ist not activated',
                        404: 'User not found'
                        }

    _responses['post'] =    {
                            200: ('Success', user_new_pw),
                            403: 'Insufficient rights e.g. secret answer is not correct',
                            404: 'User not found'
                            }


    """ send pw reset question """
    @api.doc(description='request password reset question for an user identified by id or username', responses=_responses['get'])
    @api.marshal_with(user_pwreset)
    def get(self):

        """ pw reset question for a diboard user """   
        try:
            id = request.args.get('id',default=0, type=int)
            email = request.args.get('email',default='', type=str)
            pwresetanswer = request.args.get('termsofserviceaccepted',default='', type=str)
         
        except ValueError:
            id = 0
            email = ''
            pwresetanswer = ''

        log.info('reset password question for user id:{!s} and email:{}'.format(id,email))

        """ retrieve user """
        if (id == 0) and (email == ''):
            api.abort(404, __class__._responses['get'][404])
        else:
            diboarduser = User.query.get(id)
            if (diboarduser is None):
                diboarduser = User.query.filter(User.username == email).first()
                if (diboarduser is None):
                    api.abort(404, __class__._responses['get'][404])

        """ User Active ? """
        if diboarduser.active == False:
            api.abort(403, __class__._responses['get'][403]) 

        """ prepare response """
        pwresetquestion = {'id' : diboarduser.id, 'username': diboarduser.username, 'pwresetquestion': diboarduser.pwresetquestion}
        return pwresetquestion, 200


    """ pw reset answer """
    @api.doc(description='reset password for a diboard user if the secret pw-reset answer is correct', responses=_responses['post'])
    @api.marshal_with(user_new_pw)
    def post(self):
        
        """ reset password by given pw reset answer """   
        try:
            id = request.args.get('id',default=0, type=int)
            email = request.args.get('email',default='', type=str)
            pwresetanswer = request.args.get('pwresetanswer',default='', type=str)
         
        except ValueError:
            id = 0
            email = ''
            pwresetanswer = ''

        log.info('reset password for user id:{!s} and email:{}'.format(id,email))

        """ retrieve user """
        if (id == 0) and (email == ''):
            api.abort(404, __class__._responses['get'][404])
        else:
            diboarduser = User.query.get(id)
            if (diboarduser is None):
                diboarduser = User.query.filter(User.username == email).first()
                if (diboarduser is None):
                    api.abort(404, __class__._responses['get'][404])

        """ User Active ? """
        if diboarduser.active == False:
            api.abort(403, __class__._responses['get'][403])

        """ check secret answer """
        if (not diboarduser.verify_pwresetanswer(pwresetanswer)):
            api.abort(403, __class__._responses['post'][403])

        """ reset password """
        password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        diboarduser.hash_password(password)
        db.session.add(diboarduser)
        db.session.commit()

        """ prepare response """
        pwreset = {'id' : diboarduser.id, 'username': diboarduser.username, 'password': password}
        return pwreset, 200

        
@api.route('/token')
@api.param(name = 'expiration', description = 'access token validity in seconds (default 10 min.)', type = int)
class Token(Resource):
    
    # response codes
    _responses = {200: ('token successfully generated', user_token),
                  401: 'Missing Authentification or wrong credentials',
                  403: 'Insufficient rights e.g. User ist not activated'
                 }
    
    @api.doc(description='request a user acces token for http basic auth with given expiration (default 10 min.)', security='basicauth', responses=_responses)
    @basicauth.login_required
    @api.marshal_with(user_token)
    def get(self):
        
        """ get user access token """
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
    
    """ swagger response documentation as class var """
    _responses = {}   
    _responses['get'] = {
        200: ('Success', user_subscriptions),
        401: 'Missing Authentification or wrong credentials',
        403: 'Insufficient rights',
        404: 'No Subscriptions found'
        }
    
    @api.doc(description='retrieve a list of boards the user is subscribed', security='basicauth', responses=_responses['get'])
    @basicauth.login_required
    @api.marshal_with(user_subscriptions)
    def get(self):

        """ list of boards user subscribed to """
        AuthUser = g.get('user')
        if AuthUser is None:
             api.abort(401, __class__._responses['get'][401])

        """ logging """
        log.info('select subscriptions for user: {!s}'.format(AuthUser.id))

        """ User Active ? """
        if AuthUser.active == False:
            api.abort(403, __class__._responses['get'][403]) 

        """ return auth user 
            filter subscriptions to active
            filter boards to active
        """
        subscriptionsreturn = User.query.filter(User.boards.any(Subscription.active == True)).all()


        return subscriptionsreturn, 200
