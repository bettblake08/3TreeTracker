from flask_restful import Resource,reqparse
from App.Models.LongrichUser import LongrichUserModel
from werkzeug.security import generate_password_hash

class RootLongrichUser(Resource):
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

    def post(self):
        data = RootLongrichUser.parser.parse_args()

        user = LongrichUserModel(
             name=data.name,
             surname=data.surname,
             email=data.email,
             phoneNo=data.phoneNo,
             gender=data.gender,
             nationality=data.nationality,
             placement=0,
             password=generate_password_hash(data.password))

        user.save()

        return {"error": 0}
