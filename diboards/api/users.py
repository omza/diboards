from flask import request, g
from flask import current_app as app
from flask_restplus import Namespace, Resource, fields
from .core import create_user, delete_user, update_user
from database.models import  User
from auth import auth as basicauth

# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

api = Namespace('users', description='user related operations')

# Serializers
# ----------------------------------------------------------------------
user = api.model('di.board users', {
    'id': fields.Integer(readOnly=True, required=False, description='The identifier of a user'),
    'uuid': fields.String(readOnly=True, required=False, description='The unique identifier of a bulletin board'),
    'username': fields.String(required=True, description='email'),
    'password': fields.String(required=True, description='user password', attribute='password_hash'),
    'active': fields.Boolean(required=False, description='user is activated ?'),
    'name': fields.String(required=False, description='User name'),
    'create_date': fields.DateTime(readOnly=True, required=False), 
})

# Parsers
# ----------------------------------------------------------------------



# routes
# ---------------------------------------------------------------------
@api. route('/')
class UserCollection(Resource):
    @api.doc('list_user')
    @api.marshal_list_with(user)
    def get(self):
        '''List all users'''
        userList = User.query.all()
        return userList


    @api.response(200, 'User signed successfully up.')
    @api.response(400, 'User already signed up')
    @api.expect(user)
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
        diboarduser = User.query.filter(User.uuid == uuid).one()
        if diboarduser is None:
            log.warning('Not found....Mysterious')
            api.abort(404)
        else:        
            log.info('USER: ' + AuthUser.username)
            return diboarduser, 200