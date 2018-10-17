""" This module hosts the user account blueprint. """
from flask import Blueprint
from app.api.v1.controllers import AccountController

API_V1_USER = Blueprint("API_V1_USER", __name__)

ACCOUNT_CONTROLLER = AccountController()


@API_V1_USER.route('/account/loginAuth', methods=['POST'])
def account_login_auth():
    """ This function redirects the api request to the account controller that handles
        the login authentication of the longrich account.
    """
    return ACCOUNT_CONTROLLER.login_auth()


@API_V1_USER.route('/account/logout')
def account_user_log_out():
    """ This function redirects the api request to the account controller that handles
        the logging out of the longrich account.
    """
    return ACCOUNT_CONTROLLER.log_out()
