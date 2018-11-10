""" This module hosts the main api blueprint. """

from flask import (jsonify, redirect, url_for, Blueprint)
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_refresh_token_required,
                                set_access_cookies)
from flask_restful import Api

from app.api.v1.controllers import MainController
from app.api.v1.resources import CommentReaction, Comment, LongrichUser
from app.database.models import RevokedTokenModel

API_V1_MAIN = Blueprint("API_V1_MAIN", __name__)
API = Api(API_V1_MAIN)

MAIN_CONTROLLER = MainController()

API.add_resource(
    Comment, '/comment/<string:param>/<string:param2>/<string:offset>')
API.add_resource(
    CommentReaction, '/commentReaction/<string:param>/<string:param2>/<string:param3>')

API.add_resource(LongrichUser, '/longrichAccount')


@API_V1_MAIN.route('/api/key2/refresh')
@jwt_refresh_token_required
def refresh_token():
    """ This function refreshes an expired token."""
    user = get_jwt_identity()
    resp = jsonify({
        "message": "You have successfully refreshed token!"
        })
    set_access_cookies(
        resp,
        create_access_token(
            identity=user,
            fresh=True
            )
        )
    return resp


@API_V1_MAIN.route('/getProduct/<string:param>')
def get_product(param):
    """ This function redirects the api request to the main controller that handles
        the retrieval of product data.
    """
    return MAIN_CONTROLLER.get_product(param)


@API_V1_MAIN.route('/getProducts/<string:offset>')
def get_products(offset):
    """ This function redirects the api request to the main controller that handles
        the retrieval of all products' data.
    """
    return MAIN_CONTROLLER.get_products(offset)


@API_V1_MAIN.route('/productReaction/<string:param>/<string:param2>')
def product_reaction(param, param2):
    """ This function redirects the api request to the main controller that handles
        the setting of a product reaction.
    """
    return MAIN_CONTROLLER.product_reaction(param, param2)


@API_V1_MAIN.route('/getForm')
def get_form():
    """ This function redirects the api erquest to the main controller that handles
        the retrieval of the form pdf.
    """
    return MAIN_CONTROLLER.get_form()


@API_V1_MAIN.route('/getPlacements/<string:name>')
def get_placement(name):
    """ This function redirects the api request to the main controller that handles
        the retrieval of the placement user details.
    """
    return MAIN_CONTROLLER.get_placement(name)
