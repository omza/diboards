# Flask settings
SERVER_NAME = None
DEBUG = True  # Do not use debug mode in production
PORT = 5000
HOST = 'localhost'

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.diboards'
SQLALCHEMY_TRACK_MODIFICATIONS = True
