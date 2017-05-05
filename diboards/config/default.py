# Flask settings
SERVER_NAME = 'api.diboards.com'
DEBUG = False  # Do not use debug mode in production
PORT = 5000
HOST = '0.0.0.0'

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = True

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:////usr/db/db.diboards'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# di.boards settings
DIBOARDS_PATH_QR = '/usr/qr/'
DIBOARDS_PATH_INCOMMING = '/usr/incomming/'
DIBOARDS_PATH_OUTGOING = '/usr/outgoing/'
