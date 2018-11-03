""" This module hosts the flask app configurations for different environments. """
import os


class Config(object):
    here = os.path.abspath(os.path.dirname('./'))

    WEBPACK_MANIFEST_PATH = os.path.join(here, "manifest.json")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/api/key2/'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    REPO_DIR = "public/repo/"


class ProductionConfig(Config):
    ENV = "production"
    FLASK_ENV = "development"
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True


class DevelopmentConfig(Config):
    ENV = "development"
    FLASK_ENV = "development"
    DEBUG = True
    SECRET_KEY = b'\x0c$V\x92\x1b1\x05xp@\xfa\xdc\x94\x87\xc4\x0f'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:m21c07s96@127.0.0.1/longrich'

    JWT_SECRET_KEY = b'\x0c$V\x92\x1b1\x05xp@\xfa\xdc\x94\x87\xc4\x0f'
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False


class TestingConfig(Config):
    ENV = "development"
    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:m21c07s96@127.0.0.1/longrich'

    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False


APP_CONFIG = {
    "DEFAULT":DevelopmentConfig,
    "DEV":DevelopmentConfig,
    "TEST":TestingConfig,
    "PROD":ProductionConfig
}