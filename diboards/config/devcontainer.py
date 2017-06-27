# Flask settings
SERVER_NAME = 'devdiboards.com:5000'
DEBUG = True  # Do not use debug mode in production
PORT = None
HOST = None

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:////usr/db/db.diboards'
SQLALCHEMY_TRACK_MODIFICATIONS = True
DIBOARDS_LOGLEVEL_CONSOLE = 10 # Info 
DIBOARDS_LOGLEVEL_FILE = 10 # debug