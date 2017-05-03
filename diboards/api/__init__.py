from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound

from .boards import api as boards_ns
from .apitools import api as tools_ns

# register flask_restplus api
api = Api(
    title='di.boards api',
    version='1.0',
    description='bring your real world bulletin board in digitial life',
    doc='/doc/',
    # All API metadatas
)

# register di.boards api namespace
api.add_namespace(boards_ns)
api.add_namespace(tools_ns)


def postmancollection():
    from flask import json
    
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    return json.dumps(data)



# global error handling
@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    #log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    #log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404

