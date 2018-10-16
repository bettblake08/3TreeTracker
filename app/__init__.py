""" This module hosts the function that handles the creation of
    the flask application instance.
"""
from os import path

from flask import Flask
from flask_webpack import Webpack

from db import db

from app.pages import ADMIN_PAGES, MAIN_PAGES
from app.api.v1 import API_V1_ADMIN, API_V1_MAIN, API_V1_USER

from instance.config import APP_CONFIG


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

    return app
