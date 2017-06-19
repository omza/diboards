# imports & globals
# -------------------------------------------------------------

from flask import Blueprint
from flask_restplus import Api

from api.boards import api as boards_ns
from api.users import api as users_ns
from api.tools import api as tools_ns

from sqlalchemy.orm.exc import NoResultFound
from auth import authorizations

# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)


# register flask_restplus api and namespaces as blueprint
# --------------------------------------------------------------

diboardsapi = Blueprint('api', __name__) #, url_prefix='/v0') # subdomain ='api'


api = Api(diboardsapi,
    title='di.boards api',
    version='0.1',
    description='bring your real world bulletin board in digitial life',
    #doc='/swagger/',
    # All API metadatas
    authorizations=authorizations,
    #serve_challenge_on_401 = True,
    #catch_all_404s = True,
)

# Initialize flask-restplus api
# register di.boards api namespace
api.add_namespace(boards_ns)
api.add_namespace(users_ns)
api.add_namespace(tools_ns)



# global error handling
# --------------------------------------------------------------
@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not app.config['DEBUG']:
        return {'message': message}, 500

@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404

