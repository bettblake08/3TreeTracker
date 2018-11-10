""" This module hosts the function that handles the creation of
    the flask application instance.
"""
from os import path

from flask import Flask, redirect, url_for
from flask_webpack import Webpack
from flask_jwt_extended import JWTManager

from db import db

from app.pages import ADMIN_PAGES, MAIN_PAGES
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

    app.register_blueprint(MAIN_PAGES)
    app.register_blueprint(ADMIN_PAGES, url_prefix="/admin")
    app.register_blueprint(API_V1_MAIN, url_prefix="/api/v1")
    app.register_blueprint(API_V1_ADMIN, url_prefix="/api/v1/admin")
    app.register_blueprint(API_V1_USER, url_prefix="/api/v1/user")

    webpack = Webpack()
    webpack.init_app(app)

    db.init_app(app)

    JWT = JWTManager(app)

    @JWT.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        """ This function is a jwt blacklist loader to check whether the token
            provided has been blacklisted.
        """
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_token_blacklisted(jti)


    @JWT.unauthorized_loader
    @JWT.invalid_token_loader
    @JWT.expired_token_loader
    def redirect_to_login(error):
        """ This function redirects any url call that contains an expired, 
            unauthorized or invalid token to the admin login.
        """
        return redirect(url_for("ADMIN_PAGES.admin_login_page"))

    return app
