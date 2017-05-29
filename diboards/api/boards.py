from flask import request, g, send_from_directory
from flask_restplus import Namespace, Resource

import auth
from api.core import create_board, list_boards, delete_board, read_board, update_board, create_qrcode
from api.serializers import board, qr


# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

api = Namespace('boards', description='bulletin board related operations')


# Endpoints
# ------------------------------------------------------------------------------------------------

@api.route('/')
class BoardCollection(Resource):
    
    @api.doc('list_boards', security='basicauth')
    @auth.basicauth.login_required
    @api.marshal_list_with(board)
    def get(self):
        '''List all boards'''
        log.info('get boards')
        AuthUser = g.user
        BoardList = list_boards(AuthUser)
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
class BoardItem(Resource):
    
    @api.doc('get_board')
    @api.marshal_with(board)
    @api.response(404, 'Board not found')
    def get(self, uuid):
        '''Fetch a board given its identifier'''        
        diboard = read_board(uuid)
        if diboard is None:
            return 404
        else:    
            return diboard, 200
        pass


@api.route('/<uuid>/qr')
@api.param('uuid', 'The unique identifier of a bulletin board')
class BoardQRCode(Resource):

    @api.expect(qr)
    @api.doc('get_qrcode', security='basicauth')
    @auth.basicauth.login_required
    @api.response(401, 'Authentication Required')
    @api.response(403, 'Insufficient rights')
    @api.response(404, 'board not found')
    def post(self, uuid):

        log.info('post_qrcode')
        AuthUser = g.user
        data = request.json
        
        httpstatus, filename, filepath = create_qrcode(uuid, data, AuthUser)
        
        if  httpstatus == 401:
            return 401, 'Authentication Required'
        elif httpstatus == 403:
            return 403, 'Insufficient rights'
        elif httpstatus == 404:
            return 404, 'board not found'
        elif (filename is not None) and (filepath is not None):
            # sendfile
            log.debug(filepath)
            log.debug(filename)
            return send_from_directory(filepath, filename, as_attachment=True)
        else:
            api.abort(500)


