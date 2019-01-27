""" This module hosts the flask app configurations for different environments. """
import os


class Config(object):
    here = os.path.abspath(os.path.dirname('./'))

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_REFRESH_COOKIE_PATH = '/api/key2/'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    REPO_DIR = "public/repo/"

    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    SQLALCHEMY_URI = 'postgresql://{}:{}@{}/'.format(
        DB_USER, DB_PASSWORD, DB_HOST
    )

    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_URI + DB_NAME


class ProductionConfig(Config):
    ENV = "production"
    FLASK_ENV = "production"
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_DOMAIN = os.getenv("FRONTEND_DOMAIN")


class DevelopmentConfig(Config):
    ENV = "development"
    FLASK_ENV = "development"
    DEBUG = True
    SECRET_KEY = b'\x0c$V\x92\x1b1\x05xp@\xfa\xdc\x94\x87\xc4\x0f'

    JWT_SECRET_KEY = b'\x0c$V\x92\x1b1\x05xp@\xfa\xdc\x94\x87\xc4\x0f'
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_DOMAIN = "127.0.0.1"


class TestingConfig(DevelopmentConfig):
    TESTING = True
    
    DB_NAME = os.getenv("TEST_DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    SQLALCHEMY_URI = 'postgresql://{}:{}@{}/'.format(
        DB_USER, DB_PASSWORD, DB_HOST
    )
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_URI + DB_NAME


APP_CONFIG = {
    "DEFAULT":DevelopmentConfig,
    "DEV":DevelopmentConfig,
    "TEST":TestingConfig,
    "PROD":ProductionConfig
}
