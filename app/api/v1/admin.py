""" This module hosts the admin api blueprint. """

from flask import Blueprint
from flask_jwt_extended import (jwt_refresh_token_required, jwt_required)
from flask_restful import Api

from app.api.v1.controllers import AdminController
from app.api.v1.resources import (AdminLongrichUser, AdminProduct, AdminUser, Post,
                                  RepoFile, RepoFolder, Tag,
                                  Tags, UploadAPI)


API_V1_ADMIN = Blueprint("API_V1_ADMIN", __name__)

API = Api(API_V1_ADMIN)
ADMIN_CONTROLLER = AdminController()

API.add_resource(AdminUser, '/user/<string:param>')
API.add_resource(RepoFolder, '/repoFolder/<string:param>')
API.add_resource(RepoFile, '/repoFile/<string:id>')
API.add_resource(Tag, '/tag/<string:param>')
API.add_resource(Tags, '/tags/<string:param>')
API.add_resource(Post, '/post/<string:param>')
API.add_resource(AdminLongrichUser, '/longrichAccount/<string:param>')
API.add_resource(AdminProduct, '/product/<string:param>')
API.add_resource(UploadAPI, '/uploadFiletoRepo/<uuid>')


@API_V1_ADMIN.route('/login', methods=['POST'])
def login_auth():
    """ This function redirects the api request to the admin controller that handles
        the logging in of an admin account.
    """
    return ADMIN_CONTROLLER.login_auth()


@API_V1_ADMIN.route('/logout')
@jwt_required
def admin_log_out_access():
    """ This function redirects the api request to the admin controller that handles
        the logging out of an admin user.
    """
    return ADMIN_CONTROLLER.admin_log_out()


@API_V1_ADMIN.route('/api/key2/logout')
@jwt_refresh_token_required
def log_out_refresh_token():
    """ This function redirects the api call to the admin controller that handles
        the blacklisting of the refresh token.
    """
    return ADMIN_CONTROLLER.admin_log_out()


@API_V1_ADMIN.route('/retrieveRepoContentByFolder/<string:folder>')
@jwt_required
def retrieve_repo_content_by_folder(folder):
    """ This function redirects the api call to the amdin controller that hadnles
        the retrieval of the repo folder's content.
    """
    return ADMIN_CONTROLLER.retrieve_repo_content_by_folder(folder)


@API_V1_ADMIN.route('/getData')
@jwt_required
def admin_get_data():
    """ This function redirects the api call to the admin controller that handles
        the retrieval of the admin's data.
    """
    return ADMIN_CONTROLLER.admin_data()


@API_V1_ADMIN.route('/getProducts/<string:offset>')
@jwt_required
def admin_products(offset):
    """ This function redirects the api request to the admin controller that handles
        the retrieval of all products' data.
    """
    return ADMIN_CONTROLLER.get_products(offset)


@API_V1_ADMIN.route('/getAccounts/<string:name>/<string:country>/<string:offset>')
@jwt_required
def admin_longrich_accounts(name, country, offset):
    """ This function redirects the api request to the admin controller that handles
        the retrieval of all longrich accounts.
    """
    return ADMIN_CONTROLLER.get_longrich_accounts(name, country, offset)
