""" This module hosts the user account blueprint. """
from flask import Blueprint
from app.api.v1.controllers import AccountController

API_V1_USER = Blueprint("API_V1_USER", __name__)

ACCOUNT_CONTROLLER = AccountController()


@API_V1_USER.route('/account/loginAuth', methods=['POST'])
def account_login_auth():
    return ACCOUNT_CONTROLLER.login_auth()


@API_V1_USER.route('/account/logout')
def account_user_log_out():
    return ACCOUNT_CONTROLLER.log_out()
