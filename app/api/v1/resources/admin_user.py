""" This module hosts the user api resource for the admin platform. """
from flask_restful import Resource, reqparse
from app.database.models import AdminUserModel
from werkzeug.security import generate_password_hash
from app.managers.serialization import Serialization


class AdminUser(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'username',
        required=True,
        help="The username field is required!"
        )

    parser.add_argument(
        'password',
        required=True,
        help="The password field is required!"
        )

    def post(self, param):
        """ Add New Admin User Account Endpoint """
        data = AdminUser.parser.parse_args()

        if data.username == "":
            return {
                "message": "The username value is required!"
            }, 400

        if data.password == "":
            return {
                "message": "The password value is required!"
            }, 400

        existing_user = AdminUserModel.find_by_username(data.username)

        if existing_user:
            return {
                "message": "User already exists!"
                }, 403

        if not Serialization.test_password(data.password, 1):
            return {
                "message": "Invalid password!"
            }, 400

        user = AdminUserModel(
            data.username,
            generate_password_hash(data.password)
            )

        try:
            user.save()
            return {
                "message": "You have successfully created an admin user account!"
                }, 201

        except:
            return {
                "message": "Failed to create an admin user account!"
            }, 500

    def delete(self, param):
        """ Delete Admin Account Endpoint """
        name = param
        user = AdminUserModel.find_by_username(name)

        if not user:
            return {
                "message": "Admin user does not exist!"
            }, 404

        try:
            user.delete()
            return {
                "message": "You have successfully deleted the admin account!"
            }, 200

        except:
            return {
                "message": "Failed to delete the admin account!"
            }, 500
