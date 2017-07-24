import os

from database import db
from datetime import datetime, timedelta

import database.models
import pyqrcode

from flask import current_app as app

# Logger
import logging
log = logging.getLogger('diboardapi.' + __name__)

# Bulletinboard Logic sector
# --------------------------------------



# Create Database from scratch
def reset_database():
    log.warning('try to create db from scratch')
    db.drop_all()
    db.create_all()

def postmancollection():
    from flask import json
    from api import api
    
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    return json.dumps(data)