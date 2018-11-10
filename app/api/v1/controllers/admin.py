""" This module hosts the admin controller class. """
from flask import jsonify, make_response
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_raw_jwt, set_access_cookies,
                                set_refresh_cookies, unset_jwt_cookies)
from flask_restful import reqparse

from app.database.models import (AdminUserModel, LongrichUserModel, PostModel, RepoFolderModel,
                                 RevokedTokenModel, TagModel)

from app.managers import Serialization


class AdminController:
    @staticmethod
    def authenticate(username, password):
        user = AdminUserModel.find_by_username(username)
        if user and user.authenticate(password):
            return user

    @staticmethod
    def identity(payload):
        user_id = payload["identity"]
        return AdminUserModel.find_by_id(user_id)

    @staticmethod
    def login_auth():
        """ Admin User Login Authentication Endpoint
        :args
            username    :   Username field
            password    :   Password field
        """

        parser = reqparse.RequestParser()

        parser.add_argument("username",
                            required=True,
                            help="The username field is required")

        parser.add_argument("password",
                            required=True,
                            help="The password field is required")

        data = parser.parse_args()

        response = AdminController.validate_login_data(data)

        if response:
            return make_response(response)

        current_user = AdminUserModel.find_by_username(data["username"])

        if not current_user:
            return make_response(
                jsonify({
                    "message": "User {} does not exist!".format(data["username"])
                }), 404
            )

        if not current_user.authenticate(data["password"]):
            return make_response(
                jsonify({
                    "message": "Wrong credentials!"
                }), 401
            )

        logged_in_user = {
            "id": current_user.id,
            "role": "admin"
        }

        access_token = create_access_token(
            identity=logged_in_user,
            fresh=True)

        refresh_token = create_refresh_token(identity=logged_in_user)

        resp = jsonify({
            "message": "Logged in as {}!".format(current_user.username)
        })

        set_access_cookies(resp, access_token, 900)
        set_refresh_cookies(resp, refresh_token)

        return resp, 200

    @staticmethod
    def admin_log_out():
        """ Admin User Log Out Endpoint"""
        jti = get_raw_jwt()["jti"]

        revoked_token = RevokedTokenModel(token=jti)

        try:
            revoked_token.save()

            resp = jsonify({
                "message": "Access token has been revoked!"
            })
            unset_jwt_cookies(resp)

            return resp, 200
        except:
            return make_response(
                jsonify({
                    "message": "Failed to log out admin!"
                }), 500
            )

    @staticmethod
    def admin_data():
        return jsonify({"error": 0})

    @staticmethod
    def retrieve_repo_content_by_folder(folder_id):
        """ Get Repo Folder Content Endpoint
        :args
            folder_id   :   Repo folder id
        """
        if folder_id == "root":
            content = RepoFolderModel.get_root_content(folder_id)
            return jsonify({
                "message": "You have successfully retrieved the repo content!",
                "content": content
            }), 200

        folder = RepoFolderModel.find_by_id(folder_id)

        if not folder:
            return {
                "message": "Folder does not exist!"
            }, 404

        content = folder.get_content(folder_id)
        return jsonify({
            "message": "You have successfully retrieved the repo folder content!",
            "content": content
        }), 200

    @staticmethod
    def get_products(offset):
        """ Get Products Endpoint
        :args
            offset  :   Used to paginate the list of products
        """
        posts = PostModel.get_posts_by_offset(offset)
        tags = []

        for post in posts:
            post = post.get_post()
            post_tags = post.tags

            for post_tag in post_tags:
                if post_tag.tagId not in tags:
                    tags.append(post_tag.tagId)

        tags_found = TagModel.get_all_tags(tags)
        content = []

        for post in posts:
            post_data = {}
            post = post.get_post()

            post_data["log"] = post.json()
            post_data["post"] = post.json()
            post_data["post"]["body"] = ""

            post_tags = post.tags
            post_tags_data = []

            for post_tag in post_tags:
                for tag_found in tags_found:
                    if post_tag.tagId == tag_found.id:
                        post_tags_data.append(tag_found.json())

            post_data["tags"] = post_tags_data

            content.append(post_data)

        return make_response(
            jsonify({
            "message": "You have successfully retrieved the list of posts!",
            "content": content
        }), 200)

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
            return make_response(jsonify({
                "message": "Invalid offset!"
            }), 400)

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

        return make_response(jsonify({
            "message": "You have successfully retrieved the list of user accounts!",
            "content": content
        }), 200)

    @staticmethod
    def validate_login_data(data):
        """ This function handles the validation of login inputs."""
        if len(data.username) > 30:
            return jsonify({
                "message": "Username too long. Please enter a username less than 30 characters!"
            }), 400

        if not Serialization.test_password(
                password=data.password,
                reg_type=1):
            return jsonify({
                "message": "Password is invalid!"
            }), 400
