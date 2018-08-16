from flask_restful import Resource, reqparse
from App.Models.Post import PostModel
from App.Models.ProductComment import ProductCommentModel
from App.Models.User import UserModel
from App.Models.Product import ProductModel
from flask import request

class Comment(Resource):
    def get(self,param,param2,offset):
        if int(param2) == 1:
            comments = ProductCommentModel.get_comments(
                int(param), int(offset))

            user = UserModel.find_by_user(request.remote_addr)

            if user:
                userId = user.id
            else :
                userId = ""

            return {
                "error":0,
                "content": [x.json() for x in comments],
                "userId":userId
            }

        else :
            return {"error":1}

    def post(self,param,param2,offset):
        parser = reqparse.RequestParser()

        parser.add_argument('name',
                            required=True,
                            help="The name field is required")

        parser.add_argument('email',
                            required=True,
                            help="The email field is required")

        parser.add_argument('comment',
                            required=True,
                            help="The comment field is required")

        data = parser.parse_args()
        
        try :
            post = PostModel.find_by_id(param2)

            if not post:
                return {"error" : 3}

            if int(param) == 1:
                comment = ProductCommentModel(post.postId, data.name, data.email,data.comment)
                comment.save()

                product = ProductModel.find_by_id(post.postId)
                product.comments += 1
                product.save()

                return {"error": 0}
            else :
                return {"error":2}            
        except :
            return {"error": 1, "error_msg": "Failed to post comment. Try again later!"}   


class CommentReaction(Resource):
    def get(self, param, param2,param3):
        try :
            if int(param3) <=2:
                if int(param) == 1:
                    comment = ProductCommentModel.find_by_id(int(param2))
                    print(request.remote_addr)

                    if comment :
                        comment.set_reaction(request.remote_addr, int(param3))
                        return {"error": 0}
                    else :
                        return {"error":3}

                else :
                    return {"error": 2}
            else :
                return {"error": 1}
        except:
            return {"error": 1}
