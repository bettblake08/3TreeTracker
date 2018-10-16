import json

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
        p = PostModel.find_by_id(int(param))

        if p:
            x = {}
            x['log'] = p.json()
            post = p.get_post()
            x['post'] = post.json()
            x['post']['tags'] = post.get_tags()

            return {"error": 0, "content": x}
        else:
            return {"error": 1}

    def post(self, param):

        data = AdminProduct.parser.parse_args()

        try:
            product = ProductModel(
                data.pro__title,
                data.pro__body,
                data.pro__summary,
                data.pro__image)

            product.save()

            post = PostModel(product.id, 1)
            post.save()

            image = RepoFileModel.find_by_id(data.pro__image)
            image.increase_users()

            for tag in json.loads(data.pro__tags):
                newTag = ProductTagModel(product.id, tag)
                newTag.save()

            return {"error": 0}
        except:
            return {"error": 1}

    def put(self, param):
        data = AdminProduct.parser.parse_args()

        product = ProductModel.find_by_id(param)

        if bool(product):
            if product.imageId != data.pro__image:
                product.image.decrease_users()
                image = RepoFileModel.find_by_id(data.pro__image)
                image.increase_users()

            product.title = data.pro__title
            product.body = data.pro__body
            product.summary = data.pro__summary
            product.imageId = data.pro__image
            product.save()

            ProductTagModel.update_tags(product.id, json.loads(data.pro__tags))

            try:

                return {"error": 0}
            except:
                return {"error": 2}
        else:
            return {"error": 1, "error_msg": "Product doesn't exist!"}
