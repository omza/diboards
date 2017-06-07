from flask import request, g
from flask_restplus import Namespace, Resource

from auth import basicauth
from api.core import create_user, delete_user, select_user, update_user, list_user, activate_user, list_boards
from api.serializers import user, token, newuser, userdetail, board
#from api.parsers import userparser


# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

api = Namespace('user', description='user related operations')

# routes
# ---------------------------------------------------------------------
@api.route('/')
class UserOps(Resource):
    
    # swagger responses   
    _responses = {200: ('Success', userdetail),
                  401: 'Missing Authentification or wrong credentials',
                  403: 'Insufficient rights',
                  404: 'User not found'
                  }

    _responsesNew = {200: ('User signed successfully up.', userdetail),
                        400: 'not a valid email address',
                        403: 'User already signed up'
                        }

    _responsesDelete = {200: 'Deleted',
                    401: 'Missing Authentification or wrong credentials',
                    403: 'Insufficient rights',
                    404: 'User not found'
                }

    # select user
    @api.doc(description='select/read user detail', security='basicauth', responses = _responses)
    @basicauth.login_required
    @api.marshal_with(userdetail)
    def get(self):
                
        # select user
        log.info('get_user')
        httpstatus, diboarduser =  select_user(g.user)
        
        # parse httpstatus
        if httpstatus in UserOps._responses:
            if httpstatus == 200:
                return diboarduser, 200
            else:
                api.abort(httpstatus, UserOps._responses[httpstatus])

        else:
            api.abort(500)      

    # update user
    @api.doc(description='update user', security='basicauth', responses = _responses)
    @api.expect(userdetail)
    @api.marshal_with(userdetail)
    @basicauth.login_required    
    def put(self, uuid):
        
        log.info('update user')
        
        data = request.json
        AuthUser = g.user        
        
        # Check authorized in user
        if AuthUser is None:
            log.warning('None - abort')
            return 401, 'Authentication Required'
        
        # Check User Scope
        if AuthUser.uuid != uuid:
            log.warning(AuthUser.uuid + ' != ' + uuid)
            return 403, 'Insufficient rights'

        #update user
        httpstatus = update_user(uuid, data)

        if httpstatus == 404:
            return 404, 'User not found'
        elif httpstatus == 200:
            return 200
        else:
            api.abort(500)

    # delete user
    @api.doc(description='delete an user', security='basicauth', responses = _responsesDelete)
    @basicauth.login_required
    def delete(self):
                
        # delete user
        log.debug('delete_user')
        httpstatus =  delete_user(g.user)
        
        # parse httpstatus
        if httpstatus in UserOps._responsesDelete:
            if httpstatus == 200:
                return 200, UserOps._responsesDelete[httpstatus]
            else:
                api.abort(httpstatus, UserOps._responsesDelete[httpstatus])
        else:
            api.abort(500)      
    
            
    # create user
    @api.doc(description='create a new user', responses = _responsesNew)
    @api.expect(newuser)
    @api.marshal_with(userdetail)
    def post(self):
        
        # create user
        log.info('create user')
        data = request.json
        httpstatus, diboarduser = create_user(data)
        
        # parse httpstatus
        if httpstatus in UserOps._responsesNew:
            if httpstatus == 200:
                return diboarduser, 200
            else:
                api.abort(httpstatus, UserOps._responsesNew[httpstatus])

        else:
            api.abort(500)
   
@api.route('/activate')
@api.param(name = 'id', description = 'The unique identifier of a di.board user',type = int, required=True)
@api.param(name='email', description='emailaddress to activate', type=str, required=True)
class UserActivate(Resource):

    # response codes
    _responses = {200: 'User activated', 
                  403: 'Insufficient rights or bad link', 
                  404: 'User not found', 
                  408: 'activation link is not valid anymore or user is already activated'
                  }

    @api.doc(description='this ressource/endpoint will activate the user in valid activationperiod', responses=_responses)
    def get(self):
        
        # parse request args       
        try:
            id = request.args.get('id',default=0, type=int)
            email = request.args.get('email',default='', type=str)
        except ValueError:
            id = 0
            email = ''
        
        log.debug('activate id:{!s} and email:{}'.format(id,email))

        # activate user
        httpstatus = activate_user(id, email)

        # return httpstatus, object
        if httpstatus in UserActivate._responses:
            if httpstatus == 200:
                return 200
            else:
                api.abort(httpstatus, UserActivate._responses[httpstatus])
        else:
            api.abort(500)
            

@api.route('/token')
@api.param(name = 'expiration', description = 'access token validity in seconds (default 10 min.)', type = int)
class UserToken(Resource):
    
    # response codes
    _responses = {200: ('token successfully generated', token),
                  401: 'Missing Authentification or wrong credentials'
                 }
    
    @api.doc(description='get_user_token', security='basicauth', responses=_responses)
    @basicauth.login_required
    @api.marshal_with(token)
    def get(self):
        
        #parse request args
        try:
            expiration = request.args.get('expiration',default=600, type=int)
        except ValueError:
            expiration = 600

        # generate token
        token = g.user.generate_auth_token(expiration)
        token = token.decode('ascii')
        log.debug('token {} expires in {} seconds'.format(str(token),str(expiration)))

        # prepare return
        diboardstoken = {'token' : token, 'expiration': expiration}
        return diboardstoken, 200

@api.route('/subscriptions')
class UserSubscription(Resource):
    
    # swagger responses   
    _responses = {200: ('Success', userdetail),
                  401: 'Missing Authentification or wrong credentials',
                  403: 'Insufficient rights',
                  404: 'No Boards found'
                  }
    
    @api.doc(description='retrieve a list of boards the user is subscribed', security='basicauth', responses=_responses)
    @basicauth.login_required
    @api.marshal_with(board)
    def get(self):

        # retrieve boardlist
        httpstatus, diboards = list_boards(g.user)

        # return httpstatus, object
        if httpstatus in UserActivate._responses:
            if httpstatus == 200:
                return diboards, 200
            else:
                api.abort(httpstatus, UserActivate._responses[httpstatus])
        else:
            api.abort(500)
