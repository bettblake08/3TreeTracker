from flask import render_template,jsonify
from flask_restful import reqparse
from flask_jwt_extended import jwt_required,create_access_token,create_refresh_token, get_raw_jwt, set_access_cookies,set_refresh_cookies,unset_jwt_cookies
from App.Models.RevokedToken import RevokedTokenModel
from App.Models.AdminUser import AdminUserModel
from App.Models.RepoFolder import RepoFolderModel
from App.Models.Product import ProductModel
from App.Models.Post import PostModel
from App.Models.Tag import TagModel
from App.Models.LongrichUser import LongrichUserModel

class AdminController:
    def adminLoginPage(self):
        return render_template('admin/login.html')

    def repoPage(self):
        return render_template('admin/repo.html')

    def productsPage(self):
        return render_template('admin/products.html')

    def longrichAccountsPage(self):
        return render_template('admin/accounts.html')

    @staticmethod
    def authenticate(username, password):
        user = AdminUserModel.find_by_username(username)
        if user and user.authenticate(password):
            return user

    @staticmethod
    def identity(payload):
        user_id = payload['identity']
        return AdminUserModel.find_by_id(user_id)

    @staticmethod
    def loginAuth():
        parser = reqparse.RequestParser()
        parser.add_argument('username',
                            required=True,
                            help="The username field is required")

        parser.add_argument('password',
                            required=True,
                            help="The password field is required")

        data = parser.parse_args()
        current_user = AdminUserModel.find_by_username(data['username'])

        if not current_user:
            return jsonify({"error": 1, 'message': 'User {} doesn\'t exist'.format(data['username'])})

        if current_user.authenticate(data['password']):
            access_token = create_access_token(identity=current_user.id)
            refresh_token = create_refresh_token(identity=current_user.id)

            resp = jsonify({
                'error': 0,
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token':access_token
            })

            set_access_cookies(resp,access_token,900)
            set_refresh_cookies(resp,refresh_token)

            return resp , 200
        else:
            return jsonify({'error': 2, 'message': 'Wrong credentials'})

    @staticmethod
    def adminLogOut():
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(token=jti)
            revoked_token.add()

            resp = jsonify({"error":0,'error_msg': 'Access token has been revoked'})
            unset_jwt_cookies(resp)

            return resp
        except:
            return jsonify({"error": 1, 'error_msg': 'Something went wrong'}), 500

    @staticmethod
    def adminData():
        return jsonify({'error': 0})

    @staticmethod
    def retrieveRepoContentByFolder(folderId):
        if folderId == "root":
            content = RepoFolderModel.get_root_content(folderId)
            return jsonify({"error": 0, "content": content})

        else :
            folder = RepoFolderModel.find_by_id(folderId)
            if bool(folder):
                content = folder.get_content(folderId)
                return jsonify({"error": 0, "content": content})
            else:
                return jsonify({"error":1, "error_msg":"Folder doesn't exist!"})

    @staticmethod
    def getProducts(offset):
        posts = PostModel.get_posts_by_offset(offset)
        tags = []

        for p in posts:
            post = p.get_post()
            ts = post.tags

            for t in ts:
                if t.tagId not in tags:
                    tags.append(t.tagId)

        tagsFound = TagModel.get_all_tags(tags)
        content = []

        for p in posts:
            x = {}
            post = p.get_post()

            x['log'] = p.json()
            x['post'] = post.json()
            x['post']['body'] = ""

            ts = post.tags
            xtags = []

            for t in ts:
                for y in tagsFound:
                    if t.tagId == y.id:
                        xtags.append(y.json())
            
            x['tags'] = xtags

            content.append(x)


        return {"error":0,"content":content}


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
