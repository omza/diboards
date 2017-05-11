from flask_restplus import Namespace, Resource, fields

# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

api = Namespace('core', description='di.boards core tools api endpoints')


@api. route('/resetdb')
@api.response(404, 'Could not create db')
@api.response(201, 'database successfully created.')
class ResetDatabase(Resource):
    @api.doc('create database')
    def post(self):
        '''create database from scratch'''
        try:
            from .core import reset_database
            reset_database()
            return None, 201

        except:
            return None, 404


@api. route('/postman')
#@api.response(404, 'Could not transmit postman collection')
@api.response(201, 'postman collection successfully created.')
class PostmanCollection(Resource):
    @api.doc('create postman collection')
    def get(self):
        from api import postmancollection            
        data = postmancollection()
        return data, 201

        