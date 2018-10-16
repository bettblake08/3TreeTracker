from flask_restful import Resource,reqparse
from app.database.models import LongrichUserModel
from werkzeug.security import generate_password_hash

class AdminLongrichUser(Resource):
    def post(self):
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

        try : 
            user = LongrichUserModel(
                name=data.name,
                surname=data.surname,
                email=data.email,
                phoneNo=data.phoneNo,
                gender=data.gender,
                nationality=data.nationality,
                placement=data.placement,
                password=generate_password_hash(data.password))

            user.save()

            return {"error": 0}
        except :
            return {"error": 1}


    def put(self,param):
        parser = reqparse.RequestParser()

        parser.add_argument('placementId',
                            type=int,
                            required=True,
                            help="The username field is required")

        data = parser.parse_args()

        user = LongrichUserModel.find_by_id(int(param))

        if user:
            user.placementId = data.placementId
            user.save()
            return {"error": 0}
        else:
            return {"error": 1}
