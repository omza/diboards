# Flask settings
SERVER_NAME = 'diboards.com'
DEBUG = False  # Do not use debug mode in production
PORT = None
HOST = None

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = True
BUNDLE_ERRORS = True

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:////usr/db/db.diboards'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# di.boards settings
DIBOARDS_VERSION = 'v0.1'
DIBOARDS_PATH_TERMSOFSERVICE = 'https://diboards.com/legal/diboards_agb_v201707.pdf'
DIBOARDS_PATH_UPLOAD = '/tmp/'
DIBOARDS_PATH_MESSAGE = '/usr/messages/'
DIBOARDS_PATH_QR = '/usr/qr/'
DIBOARDS_PATH_LOG = '/usr/log/'
DIBOARDS_LOGLEVEL_CONSOLE = 0 # Notset 
DIBOARDS_LOGLEVEL_FILE = 40 # Error
DIBOARDS_LOGMAXBYTE_FILE = 1000000
DIBOARDS_LOGBACKUPCOUNT_FILE = 5
DIBOARDS_APP_SCHEME = 'diboards://board/id='
