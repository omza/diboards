from flask import g
from flask_httpauth import HTTPBasicAuth
from database.models import User

# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

# HTTP Authentification
# --------------------------------------------------------------
auth = HTTPBasicAuth()

@auth.error_handler
def auth_error():
    #api.abort(401)
    log.info('authentification error callback')
    return "&lt;h1&gt;Access Denied&lt;/h1&gt;"

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        g.user = None
        return False
    g.user = user
    log.info(' VERIFIED USER: ' + user.username)
    return True

