""" This module hosts the user api resource for the admin platform. """
from flask_restful import Resource, reqparse
from app.database.models import AdminUserModel
from werkzeug.security import generate_password_hash


class AdminUser(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username',
                        required=True,
                        help="The username field is required")

    parser.add_argument('password',
                        required=True,
                        help="The password field is required")

    def post(self, param):
        """ Add New Admin User Account Endpoint """
        data = AdminUser.parser.parse_args()

        if AdminUserModel.find_by_username(data.username):
            return {
                "message": "User already exists!"
                }, 404

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
            }

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
            }

        except:
            return {
                "message": "Failed to delete the admin account!"
            }, 500
