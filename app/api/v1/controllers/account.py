""" This module hostst the user account controller class. """
from flask import jsonify, make_response
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_raw_jwt, set_access_cookies,
                                set_refresh_cookies, unset_jwt_cookies)
from flask_restful import reqparse

from app.database.models import (LongrichUserModel, RevokedTokenModel)
from app.managers import Serialization


class AccountController:
    """ This class is the account controller class that handles the api requests without 
        an api resource
    """
    @staticmethod
    def authenticate(username, password):
        user = LongrichUserModel.find_by_username(username)
        if user and user.authenticate(password):
            return user

    @staticmethod
    def identity(payload):
        user_id = payload["identity"]
        return LongrichUserModel.find_by_id(user_id)

    @staticmethod
    def login_auth():
        """ Login Authentication Endpoint
        :args
            code            :   Longrich user ID code
            usernameType    :   Username type
                                1: User email
                                2: User code
            username        :   Login username field
            password        :   User password
        """
        parser = reqparse.RequestParser()

        parser.add_argument("code",
                            required=True,
                            help="The username field is required")

        parser.add_argument("usernameType",
                            type=int,
                            required=True,
                            help="The usernameType field is required")

        parser.add_argument("username",
                            required=True,
                            help="The username field is required")

        parser.add_argument("password",
                            required=True,
                            help="The password field is required")

        data = parser.parse_args()

        if data.usernameType not in [1, 2]:
            return {
                "message": "Invalid username type!"
            }, 400

        current_user = None

        if data.usernameType == 1:
            if not Serialization.test_email(data.username):
                return {
                    "message": "Invalid email as username!"
                }

            current_user = LongrichUserModel.find_by_email(data.username)

        elif data.usernameType == 2:
            current_user = LongrichUserModel.find_by_code(data.username)

        if not current_user:
            return jsonify({
                "message": "User {} does not exist!".format(data.username)
                }), 404

        if data.usernameType == 1:
            if not current_user.verified:
                if not data.code:
                    return jsonify({
                        "message": """User {} has not been verified! """.format(data.username)
                    }), 403

                current_user.verify(data.code)

        if not current_user.authenticate(data.password):
            return make_response(jsonify({
                "message":"Wrong credentials!"
            }), 401)

        logged_in_user = {
            "id": current_user.id,
            "role": "user"
        }

        access_token = create_access_token(
            identity=logged_in_user,
            fresh=True)

        refresh_token = create_refresh_token(
            identity=logged_in_user)

        resp = jsonify({
            "message": "Logged in as {}".format(current_user.name)
        })

        set_access_cookies(resp, access_token, 900)
        set_refresh_cookies(resp, refresh_token)

        return resp, 200


    @staticmethod
    def log_out():
        """ Longrich User Log Out Endpoint """
        jti = get_raw_jwt()["jti"]

        revoked_token = RevokedTokenModel(token=jti)
        try:
            revoked_token.add()

            resp = jsonify({
                "message": "Access token has been revoked!"
                })

            unset_jwt_cookies(resp)

            return resp
        except:
            return jsonify({
                "message": "Failed to log out!"
                }), 500

    @staticmethod
    def get_longrich_accounts(name, country, offset):
        """ Get Longrich Accounts Endpoint
        :args
            name    :   Longrich user account name
            country :   Longrich user nationality 3 letter code
            offset  :   Offset for list of users, used for pagination
        """

        try:
            offset = int(offset)
        except:
            return {
                "message": "Invalid offset!"
            }, 400

        users = LongrichUserModel.get_users_by_offset(name, country, offset)
        
        placements = []
        placements_found = []

        for user in users:            
            if user.placementId not in placements:
                placements.append(user.placementId)

        if placements:
            placements_found = LongrichUserModel.get_placements(placements)

        content = []

        for user in users:
            user_data = {}
            user_data["account"] = user.json()

            for placement_found in placements_found:
                if user.placementId == placement_found.id:
                    user_data["account"]["placement"] = placement_found.json()

            content.append(user_data)

        return {
            "message" : "You have successfully retrieved the list of user accounts!",
            "content": content
            }, 200
