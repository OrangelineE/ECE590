import os
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:passwd123@localhost:5432/ece590'\
        .format(os.environ.get('DB_USER'),
                quote_plus(os.environ.get('DB_PASSWORD')),
                os.environ.get('DB_HOST'),
                os.environ.get('DB_PORT'),
                os.environ.get('DB_NAME'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False