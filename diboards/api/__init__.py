from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound

# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

# register flask_restplus api
# --------------------------------------------------------------
authorizations = {
    'basicauth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(
    title='di.boards api',
    version='1.0',
    description='bring your real world bulletin board in digitial life',
    #  doc='/doc/',
    # All API metadatas
    authorizations=authorizations,
    #serve_challenge_on_401 = True,
    #catch_all_404s = True,
)


# global error handling
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

