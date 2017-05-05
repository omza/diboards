from flask import request
from flask_restplus import Namespace, Resource, fields
from core.businesslogic import create_user, delete_user, update_user
from core.database import  User

api = Namespace('users', description='user related operations')

user = api.model('di.board users', {
    'id': fields.Integer(readOnly=True, required=False, description='The identifier of a user'),
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

    'active': fields.Boolean(required=True, description='Board is activated ?'),
    'qrcode': fields.String(required=False, description='Link to QR Code'),

    'create_date': fields.DateTime(readOnly=True, required=False), 
})


@api. route('/')
class UserCollection(Resource):
    @api.response(200, 'Bulletin Board successfully created.')
    @api.expect(user)
    @api.marshal_with(user)

    def post(self):
        data = request.json
        dibuser = create_user(data)
        return dibuser, 200


@api.route('/<uuid>')
@api.param('uuid', 'The unique identifier of a bulletin board')
@api.response(404, 'Board not found')
class BoardItem(Resource):
    @api.doc('get_board')
    @api.marshal_with(board)
    def get(self, uuid):
        '''Fetch a board given its identifier'''
        
        diboard = Board.query.filter(Board.uuid == uuid).one()
        return diboard, 200
        
        api.abort(404)