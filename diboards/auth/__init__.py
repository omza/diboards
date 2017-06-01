from flask import g, abort
from flask_httpauth import HTTPBasicAuth
from database.models import User


# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

# HTTP Authentification
# --------------------------------------------------------------
basicauth = HTTPBasicAuth()

@basicauth.error_handler
def auth_error():
    log.debug('Authentification error callback')
    abort(401, 'Missing Authentification or wrong credentials')
    return

@basicauth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

