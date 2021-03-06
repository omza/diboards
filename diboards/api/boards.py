from flask import request, g, send_from_directory, current_app as app
from flask_restplus import Namespace, Resource, fields

import auth

from database import db
from database.models import User, Board, Subscription, QRcode

import os
from datetime import datetime, timedelta
import pyqrcode

# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

api = Namespace('board', description='bulletin board related operations')

""" bord api models (object serializers)

    board = api.model(_board['name'], _board['model'])
    boarddetail = api.model(_boarddetail['name'], _boarddetail['model'])
    boardnew = api.model(_newboard['name'], _newboard['model'])
    qr = api.model(_qr['name'], _qr['model'])

"""

qr_new = api.model('Bulletin Board qrcode',{
    'width': fields.Integer(required=True, description='width of qr code in cm')#,
    #'height': fields.Integer(required=True, description='height always'),
    #'roundedges': fields.Boolean(required=True, description='qr code with rounded edges (Style)')
    })

qr_detail = api.model('Bulletin Board qrcode',{
    'width': fields.Integer(readOnly=True, required=True, description='width of qr code in mm'),
    'height': fields.Integer(readOnly=True, required=True, description='height of qr code in mm'),
    'roundedges': fields.Boolean(readOnly=True, required=True, description='qr code with rounded edges (Style)'),
    'file': fields.String(readOnly=True, required=True, description='Board description'),
    'create_date': fields.DateTime(readOnly=True, required=True)})

board_public = api.model('Bulletin Board public detail',{
    'id': fields.Integer(readOnly=True, required=False, description='The identifier of a bulletin board'),
    #'uuid': fields.String(readOnly=True, required=False, description='The unique identifier of a bulletin board'),
    'name': fields.String(required=True, description='Board name'),
    'description': fields.String(required=True, description='Board description'),
    'state': fields.String(required=True, description='Board location state'),
    'city': fields.String(required=True, description='Board location City'),
    'zip': fields.String(required=True, description='Board location zip code'),
    'street': fields.String(required=True, description='Board location street'),
    'housenumber': fields.String(required=True, description='Board location House Number'),
    'building': fields.String(required=True, description='Board location Building description'),
    
    'ownercompany': fields.String(required=True, description='Board owner Company'),
    'ownercity': fields.String(required=True, description='Board owner City'),
    'ownerstate': fields.String(required=True, description='Board owner state'),

    'gpslong': fields.Float(required=False, description='Board location gps longitude'),
    'gpslat': fields.Float(required=False, description='Board location gps latitude'),
    'gpsele': fields.Float(required=False, description='Board location gps elevation'),
    #'gpstime': fields.DateTime(required=False),

    #'active': fields.Boolean(readOnly=True, required=False, description='Board is activated ?'),
    #'qrcode': fields.String(required=False, description='Link to QR Code'),

    'create_date': fields.DateTime(readOnly=True, required=False)})

board_detail = api.model('Bulletin Board all data',{
    'id': fields.Integer(readOnly=True, required=False, description='The identifier of a bulletin board'),
    'name': fields.String(required=True, description='Board name'),
    'description': fields.String(required=True, description='Board description'),
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

    #'active': fields.Boolean(readOnly=True, required=False, description='Board is activated ?'),

    'create_date': fields.DateTime(readOnly=True, required=False),

    'allowemail': fields.Boolean(required=False, description='Messenger eMail is allowed ?'),
    'allowsms': fields.Boolean(required=False, description='Messenger SMS/MMS is allowed ?'),
    'acceptsubsrequests': fields.Boolean(required=False, description='Should the Board allow subscriptions request from user'),
                            
    'ownercompany': fields.String(required=True, description='Board owner Company'),
    'ownerfirstname': fields.String(required=True, description='Board owner first name'),
    'ownerlastname': fields.String(required=True, description='Board owner last name'),
    'ownercity': fields.String(required=True, description='Board owner City'),
    'ownerzip': fields.String(required=True, description='Board owner zip code'),
    'ownerstreet': fields.String(required=True, description='Board owner street'),
    'ownerhousenumber': fields.String(required=True, description='Board owner House Number'),
    'ownerstate': fields.String(required=True, description='Board owner state'),
    
    'qrcodes': fields.Nested(model=qr_detail, as_list=True)})

board_new = api.model('New Bulletin Board',{
    'name': fields.String(required=True, description='Board name'),
    'description': fields.String(required=True, description='Board description'),
    'state': fields.String(required=True, description='Board location state'),
    'city': fields.String(required=True, description='Board location City'),
    'zip': fields.String(required=True, description='Board location zip code'),
    'street': fields.String(required=True, description='Board location street'),
    'housenumber': fields.String(required=True, description='Board location House Number'),
    'building': fields.String(required=True, description='Board location Building description'),
                    
    #'gpslong': fields.Float(required=False, description='Board location gps longitude'),
    #'gpslat': fields.Float(required=False, description='Board location gps latitude'),
    #'gpsele': fields.Float(required=False, description='Board location gps elevation'),
    #'gpstime': fields.DateTime(required=False)
                    
    #'active': fields.Boolean(readOnly=True, required=False, description='Board is activated ?'),
    #'qrcode': fields.String(required=False, description='Link to QR Code'),
    #'create_date': fields.DateTime(readOnly=True, required=False),

    'allowemail': fields.Boolean(required=True, description='Messenger eMail is allowed ?'),
    'allowsms': fields.Boolean(required=True, description='Messenger SMS/MMS is allowed ?'),
    'acceptsubsrequests': fields.Boolean(required=True, description='Should the Board allow subscriptions request from user'),

    'ownercompany': fields.String(required=True, description='Board owner Company'),
    'ownerfirstname': fields.String(required=True, description='Board owner first name'),
    'ownerlastname': fields.String(required=True, description='Board owner last name'),
    'ownercity': fields.String(required=True, description='Board owner City'),
    'ownerzip': fields.String(required=True, description='Board owner zip code'),
    'ownerstreet': fields.String(required=True, description='Board owner street'),
    'ownerhousenumber': fields.String(required=True, description='Board owner House Number'),
    'ownerstate': fields.String(required=True, description='Board owner state')})

user_public = api.model('di.board users sign up', {
    'username': fields.String(required=True, description='email == username'),
    'name': fields.String(required=False, description='User name')})

subscription = api.model('Board Subscribers', {
    #'userid': fields.Integer(readOnly=True, required=False, description='The identifier of a user'),
    #'boardid': fields.Integer(readOnly=True, required=False, description='The identifier of a user'),
    'role': fields.String(readOnly=True, required=True, description='subscription role'),
    'flow': fields.String(readOnly=True, required=True, description='subscription process'),
    'flowstatus': fields.String(readOnly=True, required=True, description='subscription process status'),
    'create_date': fields.DateTime(readOnly=True, required=True),
    'user': fields.Nested(model=user_public, as_list=True)})

board_subscribors = board_public.clone('Bulletin Board public detail', {
    'subscriptions': fields.Nested(attribute='users',model=subscription,as_list=True)})


""" Endpoints

    / : BoardList

    /<id:int> : BoardInstance

    /<id:int>/qrcode : BoardQRCode

    /
"""

@api.route('/')
class BoardList(Resource):

    # swagger responses   
    _responses = {}
    _responses['get'] = {200: ('Success', board_public),
                  #401: 'Missing Authentification or wrong credentials',
                  403: 'Insufficient rights or Bad request',
                  404: 'No Boards found'
                  }
    _responses['post'] = {200: ('Success', board_detail),
                  401: 'Missing Authentification or wrong credentials',
                  403: 'Insufficient rights or Bad request'
                  }

    # list/filter boards (public)
    @api.doc(description='request Bulletin Boards by filter (id, address)', responses=_responses['get'])
    @api.param(name = 'id', description = 'filter for a single board with unique board id', type = int)
    @api.param(name = 'zip', description = 'filter by zip code', type = str)
    @api.param(name = 'city', description = 'filter by city name', type = str)
    @api.param(name = 'street', description = 'filter by street', type = str)
    @api.marshal_list_with(board_public)
    def get(self):

        """ list boards with filters """
        # concat filters
        boardsfilter = ''
        for key, value in request.args.items():            
            try:
                if key == 'id':
                    boardsfilter = boardsfilter + 'board.' + key + ' == ' + str(value) + ' AND '
                else:
                    boardsfilter = boardsfilter + 'board.' + key + ' == \'' + str(value) + '\' AND '
            
            except:
                api.abort(403, __class__._responses['get'][403])
        boardsfilter = boardsfilter[:-5]       
        
        log.info('retrieve board list with filters {!s}'.format(boardsfilter)) 

        """ retrieve Boards with filters """
        if Board.query.filter(Board.active, boardsfilter).count() == 0:
            api.abort(404, __class__._responses['get'][404])

        # return httpstatus, object
        boardlist = Board.query.filter(Board.active, boardsfilter).all()
        return boardlist, 200  


    #new board
    @api.doc(description='create an new Board and subscribe user as owner', security='basicauth', responses=_responses['post'])
    @auth.basicauth.login_required
    @api.expect(board_new)
    @api.marshal_with(board_detail)
    def post(self):
        
        """ create a diboard """
        
        """ retrieve authorized User """
        AuthUser = g.get('user')
        if AuthUser is None:
             api.abort(401, __class__._responses['post'][401])
        
             """ logging """
        log.info('create a new board for user: {!s}'.format(AuthUser.id))

        """ User Active ? 
        if AuthUser.active == False:
            api.abort(403, __class__._responses['post'][403])
        """        
        
        """ parse request data and init a Board instance and associate to user"""
        data = request.json
        
        board = Board(data)
        subscription = Subscription(role = 'OWNER', flow = 'CREATE', flowstatus = 'CREATED', active = True, create_date = datetime.utcnow())
        subscription.user = AuthUser
        board.users.append(subscription)

        """ db update """
        db.session.add_all([board, subscription])
        db.session.commit()

        """ create qrcodes in 4x4 and save as png file """
        qrpath = app.config['DIBOARDS_PATH_QR'] + str(board.id)
        if not os.path.exists(qrpath):
            os.makedirs(qrpath)
            os.chmod(qrpath, 0o755)
        qrpath = qrpath + '/'

        qrfile = 'qr-40x40-False.png'
        qrfull = qrpath + qrfile

        if (os.path.exists(qrfull)):
            os.remove(qrfull)

        url = pyqrcode.create(qrfull)
        url.png(qrfull, scale=10, module_color=(255, 45, 139, 255), background=(255, 255, 255, 255), quiet_zone=4)        
        
        
        qrcode = QRcode(height = 40, width = 40, roundedges = False, file = qrfile, create_date = datetime.utcnow())
        board.qrcodes.append(qrcode)

        log.info('create a new qrcode for board: {!s}'.format(board.id))

        """ db update """
        db.session.add_all([board, qrcode])
        db.session.commit()

        return board, 200


@api.route('/<int:id>')
@api.param('id', 'The unique identifier of a bulletin board')
class BoardInstance(Resource):

    # swagger responses   
    _responses = {}
    _responses['get'] = {200: ('Success', board_detail),
                  401: 'Missing Authentification or wrong credentials',
                  403: 'Insufficient rights or Bad request',
                  404: 'No Boards found'
                  }
    _responses['put'] = _responses['get']
    _responses['delete'] = {200: 'Board deleted',
                              401: 'Missing Authentification or wrong credentials',
                              403: 'Insufficient rights or Bad request',
                              404: 'No Boards found'
                              }

    
    """ retrieve board """
    @api.doc(description='show all diboard details to owner and administrator', security='basicauth', responses=_responses['get'])
    @auth.basicauth.login_required
    @api.marshal_with(board_detail)
    def get(self, id):

        """ request board detail data """

        """ retrieve authorized User """
        AuthUser = g.get('user')
        if AuthUser is None:
             api.abort(401, __class__._responses['get'][401])
        
        """ User Active ? """
        if AuthUser.active == False:
            api.abort(403, __class__._responses['get'][403])

        """ logging """
        log.info('select all board details for board: {!s}'.format(id))

        """ retrieve board """
        diboard = Board.query.get(id)
        if (diboard is None) or (not diboard.active):
            api.abort(404, __class__._responses['get'][404])

        """ check owner """
        subscription = Subscription.query.get((AuthUser.id, id))
        if subscription is None:
            api.abort(403, __class__._responses['get'][403])
        elif subscription.role not in ['OWNER', 'ADMIN']:
            api.abort(403, __class__._responses['get'][403])

        """ return dibhoard """
        return diboard, 200
    
            
    """ update board """
    @api.doc(description='update all diboard details by owner or administrator', security='basicauth', responses=_responses['put'])
    @auth.basicauth.login_required
    @api.expect(board_new)
    @api.marshal_with(board_detail)
    def put(self, id):
        
        """ update board detail data """

        """ retrieve authorized User """
        AuthUser = g.get('user')
        if AuthUser is None:
             api.abort(401, __class__._responses['put'][401])

        """ User Active ? """
        if AuthUser.active == False:
            api.abort(403, __class__._responses['put'][403])

        """ parse request data """
        data = request.json

        """ logging """
        log.info('select all board details for board: {!s}'.format(id))

        """ retrieve board """
        diboard = Board.query.get(id)
        if (diboard is None) or (not diboard.active):
            api.abort(404, __class__._responses['put'][404])

        """ check owner """
        subscription = Subscription.query.get((AuthUser.id, id))
        if subscription is None:
            api.abort(403, __class__._responses['put'][403])
        elif subscription.role not in ['OWNER', 'ADMIN']:
            api.abort(403, __class__._responses['put'][403])

        """ update all fields """
        for key, value in data.items():
            if (key in vars(diboard)):
                setattr(diboard, key, value)
    
        """ update database """
        db.session.add(diboard)
        db.session.commit()
               
        """ return diboard """
        return diboard, 200


    """ delete board """
    @api.doc(description='owner or administrator delete their board', security='basicauth', responses=_responses['delete'])
    @auth.basicauth.login_required
    def delete(self, id):
        
        """ delete/deactivate board """

        """ retrieve authorized User """
        AuthUser = g.get('user')
        if AuthUser is None:
             api.abort(401, __class__._responses['delete'][401])

        """ User Active ? """
        if AuthUser.active == False:
            api.abort(403, __class__._responses['delete'][403])       
     
        """ logging """
        log.info('deactivate board: {!s}'.format(id))

        """ retrieve board """
        diboard = Board.query.get(id)
        if (diboard is None) or (not diboard.active):
            api.abort(404, __class__._responses['delete'][404])

        """ check owner """
        subscription = Subscription.query.get((AuthUser.id, id))
        if subscription is None:
            api.abort(403, __class__._responses['delete'][403])
        elif subscription.role not in ['OWNER', 'ADMIN']:
            api.abort(403, __class__._responses['delete'][403])

        """ update active = false == Deleted and deactivate als User subscriptions  """
        diboard.active = False
        db.session.query(Subscription).filter(Subscription.roleid == 'USER').update({Subscription.active: False})

    
        """ update database """
        db.session.add(diboard)
        db.session.commit()
    
        return 200


@api.route('/<int:id>/qrcode')
@api.param('id', 'The unique identifier of a bulletin board')
class BoardQRCode(Resource):

    _responses = {}
    _responses['post'] = {200: ('Success', board_detail),
                          201: 'QR Code already exists',
                          401: 'Missing Authentification or wrong credentials',
                          403: 'Insufficient rights or Bad request',
                          404: 'board not found'}


    @api.doc('create a new qrcode for diboard', security='basicauth', responses=_responses['post'])
    @auth.basicauth.login_required
    @api.expect(qr_new)
    @api.marshal_with(board_detail)
    def post(self, id):
        """ create a new qrcode for diboard """
        
        """ retrieve authorized User """
        AuthUser = g.get('user')
        if AuthUser is None:
             api.abort(401, __class__._responses['post'][401])

        """ logging """
        log.info('create a new qrcode for board: {!s}'.format(id))

        """ User Active ? """
        if AuthUser.active == False:
            api.abort(403, __class__._responses['post'][403])

        """ retrieve board """
        diboard = Board.query.get(id)
        if (diboard is None) or (not diboard.active):
            api.abort(404, __class__._responses['post'][404])

        """ check owner """
        subscription = Subscription.query.get((AuthUser.id, id))
        if subscription is None:
            api.abort(403, __class__._responses['post'][403])
        elif subscription.role not in ['OWNER', 'ADMIN']:
            api.abort(403, __class__._responses['post'][403])

        """ parse request data and init a Board instance and associate to user"""
        data = request.get_json()
        height = data.get('height')
        width = data.get('width')
        roundedges = data.get('roundedges')

        if (height == 0) or (width == 0):
            api.abort(403, __class__._responses['post'][403])

        """ check if qrcode exist ? """
        """ for a kickstart only height = width and roundedges = False supported """

        qrcode = QRcode.query.filter(QRcode.board_id == id, QRcode.height == width, QRcode.width == width, QRcode.roundedges == False).first()
        if not qrcode is None:
            return diboard, 201

        """ create qrcodes and save as png file """
        qrpath = app.config['DIBOARDS_PATH_QR'] + str(id)
        if not os.path.exists(qrpath):
            os.makedirs(qrpath)
            os.chmod(qrpath, 0o755)
        qrpath = qrpath + '/'

        qrfile = 'qr-' + str(width) + 'x' + str(width) + '-' + str(roundedges) + '.png'
        qrfull = qrpath + qrfile

        if (os.path.exists(qrfull)):
            os.remove(qrfull)
        
        """ qr content deep link """
        qrcontent = app.config['DIBOARDS_APP_SCHEME'] + format(id,'05d')
        url = pyqrcode.create(content=qrcontent.upper(), error='H', version=8)
        url.png(qrfull, scale=width, module_color=(255, 45, 139, 255), background=(255, 255, 255, 255), quiet_zone=4)        
       
        qrcode = QRcode(height = height, width = width, roundedges = roundedges, file = qrfile, create_date = datetime.utcnow())
        diboard.qrcodes.append(qrcode)

        log.info('create a new qrcode for board: {!s}'.format(diboard.id))

        """ db update """
        db.session.add_all([diboard, qrcode])
        db.session.commit()

        return diboard, 200


@api.route('/<int:id>/subscribers')
@api.param('id', 'The unique identifier of a bulletin board')
class BoardSubscribers(Resource):

    _responses = {}
    _responses['get'] = {200: ('Success', board_subscribors),
                          401: 'Missing Authentification or wrong credentials',
                          403: 'Insufficient rights or Bad request',
                          404: 'No Subscriptions found'}


    @api.doc('retrieve all users who subscribed this board', security='basicauth', responses=_responses['get'])
    @auth.basicauth.login_required
    @api.marshal_with(board_subscribors)
    def get(self, id):
        """ retrieve all Board Subscribers """
        
        """ retrieve authorized User """
        AuthUser = g.get('user')
        if AuthUser is None:
             api.abort(401, __class__._responses['get'][401])

        """ logging """
        log.info('retrieve all Board Subscribers for board: {!s}'.format(id))

        """ User Active ? """
        if AuthUser.active == False:
            api.abort(403, __class__._responses['get'][403])

        """ retrieve board """
        diboard = Board.query.get(id)
        if (diboard is None) or (not diboard.active):
            api.abort(404, __class__._responses['get'][404])

        """ check owner """
        subscription = Subscription.query.get((AuthUser.id, id))
        if subscription is None:
            api.abort(403, __class__._responses['get'][403])
        elif subscription.role not in ['OWNER', 'ADMIN']:
            api.abort(403, __class__._responses['get'][403])

        """ return auth user 
            filter subscriptions to active
            filter boards to active
        """

        return diboard, 200

