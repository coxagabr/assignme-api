import os

basedir = os.path.abspath(os.path.dirname(__file__))
POSTGRES_URL = 'localhost:5432'
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'postgres'
POSTGRES_DB = 'assignme_dev'

class Config:
    # BASE CONFIG
    SECRET_KEY = '%yaoroe$abifz4%58yd1kxea6j&2y13i!3dby0wo)i0nmwxyne'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    uri_template = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'
    SQLALCHEMY_DATABASE_URI = uri_template.format(
        user=POSTGRES_USER,
        pw=POSTGRES_PASSWORD,
        url=POSTGRES_URL,
        db=POSTGRES_DB)
    
class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True