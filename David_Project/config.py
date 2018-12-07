import os

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
UPLOADS_DEFAULT_DEST = os.getcwd()
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'doc','docx'])
DEBUG = True

SECRET_KEY = 'RandomKey'
MAIL_SERVER =  'smtp.gmail.com'
BASE_HOST_NAME = "0.0.0.0"
