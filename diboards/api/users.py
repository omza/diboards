from flask import request, g
from flask_restplus import Namespace, Resource

from auth import basicauth
from api.core import create_user, delete_user, read_user, update_user, list_user
from api.serializers import user, token
from api.parsers import userparser


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
    @api.response(400, 'User already signed up')
    @api.expect(userparser)
    @api.marshal_with(user)
    def post(self):
        data = request.json
        diboarduser = create_user(data)
        if diboarduser is None:
            api.abort(400, 'User already signed up')
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
