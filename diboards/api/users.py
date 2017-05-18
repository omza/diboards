from flask import request, g
from flask_restplus import Namespace, Resource

from auth import basicauth
from api.core import create_user, delete_user, read_user, update_user, list_user
from api.serializers import user, token, newuser
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
    @api.marshal_with(user)
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
    @api.doc('get_user', security='basicauth')
    @api.marshal_with(user)
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

@api.route('/<uuid>/activate/<email>')
@api.param('uuid', 'The unique identifier of a di.board user')
@api.param('email', 'emailaddress to activate')
class UserActivate(Resource):
    @api.doc('post_user_activate')
    @api.response(200, 'User activated')
    @api.response(403, 'Insufficient rights')
    @api.response(404, 'User not found')
    
    def post(self, uuid, email):
        
        log.debug('post_user_activate')
        
        # retrieve user    
        diboarduser = read_user(uuid)
        
        if diboarduser is None:
            log.warning('User not found')
            api.abort(404)

        elif diboarduser.username != email:        
            log.warning('User not found')
            api.abort(403)

        else:
            try:    
                data = {'active' : True}
                update_user(uuid, data)
                return 200
            except:
                api.abort(500)
        pass





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
