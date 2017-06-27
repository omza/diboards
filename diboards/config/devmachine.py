# Flask settings
SERVER_NAME = 'devdiboards.com:5000'
DEBUG = True  # Do not use debug mode in production
PORT = 5000
HOST = '0.0.0.0'

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///database/db.diboards'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# di.boards settings
DIBOARDS_PATH_QR = 'C:/Users/omza/Downloads/diboards/qr/'
DIBOARDS_PATH_INCOMMING = 'C:/Users/omza/Downloads/diboards/incomming/'
DIBOARDS_PATH_OUTGOING = 'C:/Users/omza/Downloads/diboards/outgoing/'
DIBOARDS_PATH_LOG = 'C:/Users/omza/Downloads/diboards/log/'
DIBOARDS_LOGLEVEL_CONSOLE = 10 # debug 
DIBOARDS_LOGLEVEL_FILE = 10 # debug