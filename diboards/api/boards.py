from flask import request, g, send_from_directory
from flask_restplus import Namespace, Resource

import auth
from api.core import create_board, list_boards, delete_board, read_board, update_board, create_qrcode
from api.serializers import _board, _qr, _newboard, _boarddetail


# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

api = Namespace('boards', description='bulletin board related operations')

board = api.model(_board['name'], _board['model'])
boarddetail = api.model(_boarddetail['name'], _boarddetail['model'])
boardnew = api.model(_newboard['name'], _newboard['model'])

qr = api.model(_qr['name'], _qr['model'])



# Endpoints
# ------------------------------------------------------------------------------------------------

@api.route('/')
class BoardCollection(Resource):

    # swagger responses   
    _responses = {}
    _responses['get'] = {200: ('Success', board),
                  401: 'Missing Authentification or wrong credentials',
                  403: 'Insufficient rights or Bad request',
                  404: 'No Boards found'
                  }
    _responses['post'] = {200: ('Success', boarddetail),
                  401: 'Missing Authentification or wrong credentials',
                  403: 'Insufficient rights or Bad request'
                  }

    # list/filter boards (public)
    @api.doc(description='list boards with filters', responses=_responses['get'])
    @api.param(name = 'id', description = 'filter for a single board with unique board id', type = int)
    @api.marshal_list_with(board)
    def get(self):

        #retrieve boardlist
        httpstatus, diboards = list_boards(request.args.copy())

        # return httpstatus, object
        if httpstatus in BoardCollection._responses['get']:
            if httpstatus == 200:
                return diboards, 200
            else:
                api.abort(httpstatus, BoardCollection._responses['get'][httpstatus])
        else:
            api.abort(500)

    #new board
    @api.doc(description='create a new diboard', security='basicauth', responses=_responses['post'])
    @auth.basicauth.login_required
    @api.expect(boardnew)
    @api.marshal_with(boarddetail)
    def post(self):
        
        AuthUser = g.user
        data = request.json
        
        httpstatus ,diboards = create_board(data, AuthUser)

        # return httpstatus, object
        if httpstatus in BoardCollection._responses['post']:
            if httpstatus == 200:
                return diboards, 200
            else:
                api.abort(httpstatus, BoardCollection._responses['post'][httpstatus])
        else:
            api.abort(500)


@api.route('/<int:id>')
@api.param('id', 'The unique identifier of a bulletin board')
class BoardItem(Resource):

    # swagger responses   
    _responses = {}
    _responses['get'] = {200: ('Success', boarddetail),
                  401: 'Missing Authentification or wrong credentials',
                  403: 'Insufficient rights or Bad request',
                  404: 'No Boards found'
                  }
    _responses['put'] = _responses['get']

    
    """ retrieve board """
    @api.doc(description='show all diboard details to owner and administrator', security='basicauth', responses=_responses['get'])
    @auth.basicauth.login_required
    @api.marshal_with(boarddetail)
    def get(self, id):
        AuthUser = g.user
        httpstatus, diboard = read_board(id, AuthUser )

        # return httpstatus, object
        if httpstatus in BoardCollection._responses['get']:
            if httpstatus == 200:
                return diboard, 200
            else:
                api.abort(httpstatus, BoardCollection._responses['get'][httpstatus])
        else:
            api.abort(500)
    
            
    """ update board """
    @api.doc(description='update all diboard details by owner or administrator', security='basicauth', responses=_responses['put'])
    @auth.basicauth.login_required
    @api.expect(boardnew)
    @api.marshal_with(boarddetail)
    def put(self, id):
        
        AuthUser = g.user
        data = request.json

        httpstatus, diboard = update_board(id, data, AuthUser)

        # return httpstatus, object
        if httpstatus in BoardCollection._responses['put']:
            if httpstatus == 200:
                return diboard, 200
            else:
                api.abort(httpstatus, BoardCollection._responses['put'][httpstatus])
        else:
            api.abort(500)


@api.route('/<int:id>/qr')
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


