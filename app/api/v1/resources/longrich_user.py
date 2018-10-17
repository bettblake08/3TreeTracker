""" This module hosts the longrich user api resource. """
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from app.database.models import LongrichUserModel
from app.managers import Serialization


class LongrichUser(Resource):
    """ This class is the longrich user api resource. """
    parser = reqparse.RequestParser()

    parser.add_argument('name',
                        required=True,
                        help="The username field is required")

    parser.add_argument('surname',
                        required=True,
                        help="The username field is required")

    parser.add_argument('email',
                        required=True,
                        help="The username field is required")

    parser.add_argument('phoneNo',
                        required=True,
                        help="The username field is required")

    parser.add_argument('gender',
                        type=int,
                        required=True,
                        help="The username field is required")

    parser.add_argument('nationality',
                        required=True,
                        help="The username field is required")

    parser.add_argument('password',
                        required=True,
                        help="The username field is required")

    parser.add_argument('placement',
                        type=int,
                        required=True,
                        help="The username field is required")
    
    parser.add_argument('role',
                        type=int,
                        required=True,
                        help="The role field is required")

    def post(self):
        """ Post New Longrich User Endpoint
        :parameters
            name        :   Name of longrich user
            surname     :   Surname/Family name of longrich user
            email       :   Email of longrich user
            phoneNo     :   Phone number of longrich user
            gender      :   Gender of Longrich user. (Male:0, Female:1)
            nationality :   Country 3 letter code
            password    :   Password for user account
            placement   :   Longrich user id for new user to be placed under
            role        :   Set if account is root account or not
        """
        data = LongrichUser.parser.parse_args()

        if not Serialization.test_email(data.email):
            return {
                "message": "Invalid email address!"
            }, 400

        if not Serialization.test_password(
                password=data.password,
                reg_type=1):
            return{
                "message": "Invalid password!"
            }, 400

        if data.role not in [0, 1]:
            return {
                "message": "Invalid role id!"
            }, 400

        if LongrichUserModel.find_by_email(data.email):
            return {
                "message": "Email already exists!"
            }, 403
        
        placement = LongrichUserModel.find_placement(data.placement)

        if not placement:
            return {
                "message": "Placement user not found!"
            }, 404

        placement_id = 0

        if data.role == 1:
            placement_id = placement.id

        user = LongrichUserModel(
            name=data.name,
            surname=data.surname,
            email=data.email,
            phoneNo=data.phoneNo,
            gender=data.gender,
            nationality=data.nationality,
            placement=placement_id,
            password=generate_password_hash(data.password))

        try:
            user.save()
            return {
                "message": "You have successfully create a new longrich user account!",
                "content": {
                    "placement": placement.json()
                }
            }, 201

        except:
            return {
                "message": "Failed to create a new user!"
            }, 500
