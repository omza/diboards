from flask import request, g
from flask_restplus import Namespace, Resource

from auth import basicauth
from api.core import create_user, delete_user, read_user, update_user, list_user, activate_user
from api.serializers import user, token, newuser, userdetail
#from api.parsers import userparser


# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

api = Namespace('users', description='user related operations')

# routes
# ---------------------------------------------------------------------
@api.route('/')
class UserCollection(Resource):
    @api.doc('list_user', security='basicauth')
    @api.marshal_list_with(user)
    @basicauth.login_required
    def get(self):
        '''List all users'''
        log.info('request user list')
        AuthUser = g.user
        userList = list_user(AuthUser)
        return userList


    @api.response(200, 'User signed successfully up.')
    @api.response(400, 'not a valid email address')
    @api.response(403, 'User already signed up')
    @api.expect(newuser)
    @api.marshal_with(userdetail)
    def post(self):
        
        data = request.json
        httpstatus, diboarduser = create_user(data)
        
        if httpstatus == 400:
            api.abort(400, 'not a valid email address')
        elif httpstatus == 403:
            api.abort(403, 'User already signed up')
        elif diboarduser is None:
            api.abort(500)
        else:
            return diboarduser, 200


@api.route('/<uuid>')
@api.param('uuid', 'The unique identifier of a di.board user')
@api.response(401, 'Authentication Required')
@api.response(403, 'Insufficient rights')
@api.response(404, 'User not found')
class UserItem(Resource):
    @api.doc('select/read user detail', security='basicauth')
    @api.marshal_with(userdetail)
    @basicauth.login_required
    def get(self, uuid):
        log.info('get_user')
        AuthUser = g.user        
        
        # Check authorized in user
        if AuthUser is None:
            log.warning('None - abort')
            api.abort(401)
        
        # Check User Scope
        if AuthUser.uuid != uuid:
            log.warning(AuthUser.uuid + ' != ' + uuid)
            api.abort(403)
        
        # retrieve user    
        diboarduser = read_user(uuid)
        if diboarduser is None:
            log.warning('Not found....Mysterious')
            api.abort(404)
        else:        
            log.info('USER: ' + AuthUser.username)
            return diboarduser, 200

    @api.doc('update user', security='basicauth')
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



@api.route('/<uuid>:<email>/activate')
@api.param('uuid', 'The unique identifier of a di.board user')
@api.param('email', 'emailaddress to activate')
class UserActivate(Resource):
    @api.doc('this ressource/endpoint will activate the user in valid activationperiod')
    @api.response(200, 'User activated')
    @api.response(403, 'Insufficient rights')
    @api.response(404, 'User not found')
    @api.response(408, 'activation link is not valid anymore')
    def get(self, uuid, email):
        
        log.debug('activate user')
        
        # retrieve user    
        httpstatus, diboarduser = activate_user(uuid, email)
        
        if httpstatus == 403:
            api.abort(403, 'Insufficient rights')
        elif httpstatus == 404:
            api.abort(404, 'User not found')
        elif httpstatus == 408:
            api.abort(408, 'activation link is not valid anymore')
        elif diboarduser is None:
            api.abort(500)
        else:
            return 200


@api.route('/token')
class UserToken(Resource):
    @api.doc('get_user_token', security='basicauth')
    @api.response(200, 'token successfully generated')
    @basicauth.login_required
    @api.marshal_with(token)
    def get(self):
        token = g.user.generate_auth_token()
        token = token.decode('ascii')
        return {"token" : token}, 200
        pass
