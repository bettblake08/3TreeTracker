""" This module hosts the comment and comment reaction api resource used in 
    the commenting system.
"""
from flask import request
from flask_restful import Resource, reqparse

from app.database.models import (PostModel, ProductCommentModel, ProductModel,
                                 UserModel)


class Comment(Resource):
    """ This class is the comment api resource used to post, update or retrieve comments. """
    def get(self, param, param2, offset):
        """ Get Comments Endpoint
        :args
            param:  Post id
            param2: Post type
            offset: The offset of the list of comments to retrieve
        """

        try:
            post_type = int(param2)
            post_id = int(param)
            comments_offset = int(offset)

        except:
            return {
                "message": "Invalid request. Please provide integers as the three parameters!"
            }, 500

        if post_type not in [1]:
            return {
                "message": "Incorrect post type!"
            }, 400

        if post_type == 1:
            comments = ProductCommentModel.get_comments(
                post_id,
                comments_offset)

            user = UserModel.find_by_user(request.remote_addr)
            user_id = ""

            if user:
                user_id = user.id

            return {
                "message": "You have successfully retrieved the list of comments!",
                "content": [comment.json() for comment in comments],
                "userId": user_id
            }, 200


    def post(self, param, param2, offset):
        """ Post A New Comment Endpoint
        :args
            param:  Post id
            param2: Post type
            offset: The offset of the list of comments to retrieve
        """
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

        try:
            post_type = int(param2)
            post_id = int(param)

        except:
            return {
                "message": "Invalid request. Please provide integers as the three parameters!"
            }, 500

        post = PostModel.find_by_id(post_id)

        if not post:
            return {
                "message": "Post not found!"
                }, 404

        if post_type not in [1]:
            return {
                "message": "Incorrect post type!"
            }, 400

        comment = ProductCommentModel(
            post.postId,
            data.name,
            data.email,
            data.comment
            )

        product = ProductModel.find_by_id(post.postId)
        product.comments += 1

        if post_type == 1:
            try:    
                comment.save()
                product.save()

                return {
                    "message": "You have successfully posted a new comment!"
                    }, 201

            except:
                return {
                    "message": "Failed to post comment!"
                    }, 500


class CommentReaction(Resource):
    """ This class is the comment reaction api resource."""
    def get(self, param, param2, param3):
        """ Set Comment Reaction Endpoint
        :args
            param:  Post id
            param2: Post type
            comment_reaction    :   The comment reaction id
        """

        try:
            post_type = int(param2)
            post_id = int(param)
            comment_reaction = int(param3)

        except:
            return {
                "message": "Invalid request. Please provide integers as the three parameters!"
            }, 500

        if post_type not in [1]:
            return {
                "message": "Incorrect post type!"
            }, 400

        comment = ProductCommentModel.find_by_id(post_id)

        if not comment:
            return {
                "message": "Comment not found!"
                }, 404

        try:
            if post_type == 1:
                comment.set_reaction(request.remote_addr, comment_reaction)

                return {
                    "message": "You have successfully set a new reaction for the comment!"
                }, 200

        except:
            return {
                "message": "Failed to set a new reaction for the comment!"
            }, 500
