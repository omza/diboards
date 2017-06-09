from flask import request, g, send_from_directory
from flask_restplus import Namespace, Resource

import auth
from api.core import create_board, list_boards, delete_board, read_board, update_board, create_qrcode
from api.serializers import _board, _qr


# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

api = Namespace('boards', description='bulletin board related operations')

board = api.model(_board['name'], _board['model'])
qr = api.model(_qr['name'], _qr['model'])



# Endpoints
# ------------------------------------------------------------------------------------------------

@api.route('/')
class BoardCollection(Resource):

    # swagger responses   
    _responses = {200: ('Success', board),
                  401: 'Missing Authentification or wrong credentials',
                  403: 'Insufficient rights or Bad request',
                  404: 'No Boards found'
                  }

    # list/filter boards (public)
    @api.doc(description='list boards with filters', responses=_responses)
    @api.param(name = 'id', description = 'filter for a single board with unique board id', type = int)
    @api.marshal_list_with(board)
    def get(self):

        #retrieve boardlist
        httpstatus, diboards = list_boards(request.args.copy())

        # return httpstatus, object
        if httpstatus in BoardCollection._responses:
            if httpstatus == 200:
                return diboards, 200
            else:
                api.abort(httpstatus, BoardCollection._responses[httpstatus])
        else:
            api.abort(500)

    #new board
    @api.expect(board)
    @api.marshal_with(board)
    def post(self):
        data = request.json
        diboards = create_board(data)
        return diboard, 200


@api.route('/<int:id>')
@api.param('id', 'The unique identifier of a bulletin board')
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


