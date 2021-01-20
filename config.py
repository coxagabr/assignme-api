import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # BASE CONFIG
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    uri_template = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'
    SQLALCHEMY_DATABASE_URI = 'postgres://mvtmakidovwrsg:4c3662ba536618c41725313ab283c798c7d7e31d7fcd13c687c10a0ec14af559@ec2-54-225-18-166.compute-1.amazonaws.com:5432/d1at222iravvnp'
    
class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True