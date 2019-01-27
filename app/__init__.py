""" This module hosts the function that handles the creation of
    the flask application instance.
"""
from os import path

from flask import Flask, redirect, url_for
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.database.db import DATABASE

from app.api.v1 import API_V1_ADMIN, API_V1_MAIN, API_V1_USER

from instance.config import APP_CONFIG
from app.database.models import RevokedTokenModel


def create_app(config_name):
    """ This function handles the creation of a flask application instance.
    :args
        config_name :   A dict Key for the app configurations.
                        ['DEV', 'TEST', 'PROD', 'DEFAULT']
    :returns
        Flask app   :   An instance of the flask application
    """
    template_dir = path.abspath('./app/templates/')

    app = Flask(__name__, template_folder=template_dir)

    app.config.from_object(APP_CONFIG[config_name])

    app.register_blueprint(API_V1_MAIN, url_prefix="/api/v1")
    app.register_blueprint(API_V1_ADMIN, url_prefix="/api/v1/admin")
    app.register_blueprint(API_V1_USER, url_prefix="/api/v1/user")

    DATABASE.init_app(app)

    cors = CORS(app, 
        resources={r"/api/*": {
            "origins": "*"
            }}
    )

    JWT = JWTManager(app)

    @JWT.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        """ This function is a jwt blacklist loader to check whether the token
            provided has been blacklisted.
        """
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_token_blacklisted(jti)

    return app
