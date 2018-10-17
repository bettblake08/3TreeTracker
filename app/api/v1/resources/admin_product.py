import json

""" This modules hosts the product api resource for the admin platform. """
from flask import request
from flask_restful import Resource, reqparse

from app.database.models import (PostModel, ProductModel, ProductTagModel,
                                 RepoFileModel)


class AdminProduct(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('pro__title',
                        required=True,
                        help="The title field is required")

    parser.add_argument('pro__body',
                        required=True,
                        help="The body field is required")

    parser.add_argument('pro__summary',
                        required=True,
                        help="The summary field is required")

    parser.add_argument('pro__image',
                        required=True,
                        help="The image field is required")

    parser.add_argument('pro__tags',
                        required=True,
                        help="The tags field is required")

    def get(self, param):
        """ Get Product Endpoint """
        post = PostModel.find_by_id(int(param))

        if post:
            post_data = {}
            post_data['log'] = post.json()
            post = post.get_post()
            post_data['post'] = post.json()
            post_data['post']['tags'] = post.get_tags()

            return {
                "message": 0,
                "content": post_data
                }, 200

        return {
            "message": "Post does not exist!"
        }, 404


    def post(self, param):
        """ Post a New Product Endpoint """

        data = AdminProduct.parser.parse_args()

        product = ProductModel(
            data.pro__title,
            data.pro__body,
            data.pro__summary,
            data.pro__image)

        try:
            image = RepoFileModel.find_by_id(data.pro__image)

            if not image:
                return {
                    "message":"Image not found!"
                }, 404
            
            image.increase_users()

            product.save()

            post = PostModel(product.id, 1)
            post.save()

            for tag in json.loads(data.pro__tags):
                new_tag = ProductTagModel(product.id, tag)
                new_tag.save()

            return {
                "message": "You have successfully posted a new product!"
                }, 201

        except:
            return {
                "message": "Failed to post a new product!"
                }, 500

    def put(self, param):
        """ Update Product Endpoint """
        data = AdminProduct.parser.parse_args()

        product = ProductModel.find_by_id(param)

        if not product:
            return {
                "message": "Product doesn't exist!"
                }, 404

        if product.imageId != data.pro__image:
            product.image.decrease_users()
            image = RepoFileModel.find_by_id(data.pro__image)
            image.increase_users()

        product.title = data.pro__title
        product.body = data.pro__body
        product.summary = data.pro__summary
        product.imageId = data.pro__image

        ProductTagModel.update_tags(product.id, json.loads(data.pro__tags))

        try:
            product.save()
            return {
                "message": "You have successfully updated the product!"
                }, 200

        except:
            return {
                "message": "Failed to update the product!"
                }, 500
