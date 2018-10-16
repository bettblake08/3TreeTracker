from App.Models.LongrichUser import LongrichUserModel
from App.Models.Post import PostModel
from App.Models.Product import ProductModel
from App.Models.RevokedToken import RevokedTokenModel
from flask import render_template, jsonify
from flask_restful import reqparse
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_raw_jwt, set_access_cookies, set_refresh_cookies, unset_jwt_cookies


class AccountController:
    def home(self):
        return render_template("main/home.html")

    @staticmethod
    def authenticate(username, password):
        user = LongrichUserModel.find_by_username(username)
        if user and user.authenticate(password):
            return user

    @staticmethod
    def identity(payload):
        user_id = payload['identity']
        return LongrichUserModel.find_by_id(user_id)

    @staticmethod
    def loginAuth():
        parser = reqparse.RequestParser()

        parser.add_argument('code',
                            required=True,
                            help="The username field is required")

        parser.add_argument('usernameType',
                            type=int,
                            required=True,
                            help="The usernameType field is required")

        parser.add_argument('username',
                            required=True,
                            help="The username field is required")

        parser.add_argument('password',
                            required=True,
                            help="The password field is required")

        data = parser.parse_args()

        if data.usernameType == 1:
            current_user = LongrichUserModel.find_by_email(data.username)

            if not current_user:
                return jsonify({"error": 1, 'message': 'User {} doesn\'t exist'.format(data.username)})

            if not current_user.verified:
                if len(data.code) <= 0:
                    return jsonify({    
                        "error": 2, 
                        'message': 'User {} has not been verified. Please provide an account code if this is the first time.'.format(data.username)})
                
                current_user.verify(data.code)

        elif data.usernameType == 2:
            current_user = LongrichUserModel.find_by_code(data.username)

            if not current_user:
                return jsonify({"error": 4, 'message': 'A user with the account code {} doesn\'t exist'.format(data.username)})

        else :
            return jsonify({"error": 5, 'message': 'Invalid username Type'})
        

        if current_user.authenticate(data.password):
            access_token = create_access_token(identity=current_user.id)
            refresh_token = create_refresh_token(identity=current_user.id)

            resp = jsonify({
                'error': 0,
                'message': 'Logged in as {}'.format(current_user.name)
            })

            set_access_cookies(resp, access_token, 900)
            set_refresh_cookies(resp, refresh_token)

            return resp, 200
        else:
            return jsonify({'error': 3, 'message': 'Wrong credentials'})


    @staticmethod
    def userLogOut():
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(token=jti)
            revoked_token.add()

            resp = jsonify(
                {"error": 0, 'error_msg': 'Access token has been revoked'})
            unset_jwt_cookies(resp)

            return resp
        except:
            return jsonify({"error": 1, 'error_msg': 'Something went wrong'}), 500

    @staticmethod
    def getLongrichAccounts(name,country,offset):
        users = LongrichUserModel.get_users_by_offset(name,country,offset)
        placements = []

        for u in users:            
            if u.placementId not in placements:
                placements.append(u.placementId)

        placementsFound = LongrichUserModel.get_placements(placements)
        content = []

        for u in users:
            x = {}
            x['account'] = u.json()

            for y in placementsFound:
                if u.placementId == y.id:
                    x['account']['placement'] = y.json()
            
            content.append(x)


        return {"error":0,"content":content}

