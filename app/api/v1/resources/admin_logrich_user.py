from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from app.database.models import LongrichUserModel


class AdminLongrichUser(Resource):
    def post(self):
        """ Add Longrich User Account Endpoint """
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

        data = parser.parse_args()

        user = LongrichUserModel(
            name=data.name,
            surname=data.surname,
            email=data.email,
            phoneNo=data.phoneNo,
            gender=data.gender,
            nationality=data.nationality,
            placement=data.placement,
            password=generate_password_hash(data.password)
            )

        try:
            user.save()

            return {
                "message": "You have successfully created a longrich account!"
                }, 201
        except:
            return {
                "message": "Failed to create a user account!"
                }, 500

    def put(self, param):
        """ Update Longrich User Account Placement User Enpoint """
        parser = reqparse.RequestParser()

        parser.add_argument('placementId',
                            type=int,
                            required=True,
                            help="The username field is required")

        data = parser.parse_args()

        user = LongrichUserModel.find_by_id(int(param))

        if not user:
            return {
                "message": "User does not exist!"
                }, 404

        user.placementId = data.placementId

        try:
            user.save()
            return {
                "message": "You have successfully updated the user placement id!"
            }, 200

        except:
            return {
                "message":"Fialed to update user placement id!"
            }, 500
