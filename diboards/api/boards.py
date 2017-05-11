from flask import request
from flask_restplus import Namespace, Resource, fields
from .core import create_board, update_board, delete_board
from database.models import Board

# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

api = Namespace('boards', description='bulletin board related operations')

board = api.model('Bulletin Board', {
    'id': fields.Integer(readOnly=True, required=False, description='The identifier of a bulletin board'),
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
class BoardCollection(Resource):
    @api.doc('list_boards')
    @api.marshal_list_with(board)
    def get(self):
        '''List all boards'''
        BoardList = Board.query.all()
        return BoardList

    @api.response(200, 'Bulletin Board successfully created.')
    @api.expect(board)
    @api.marshal_with(board)
    def post(self):
        data = request.json
        diboard = create_board(data)
        return diboard, 200


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
