from flask_restful import Resource, reqparse
from App.Models.Product import ProductModel
from App.Models.ProductTag import ProductTagModel
from App.Models.Post import PostModel
from App.Models.RepoFile import RepoFileModel
from App.Models.Post import PostModel

from flask import request
import json

class AdminProduct(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('art__title',
                        required=True,
                        help="The title field is required")

    parser.add_argument('art__author',
                        required=True,
                        help="The author field is required")

    parser.add_argument('art__body',
                         required=True,
                         help="The body field is required")

    parser.add_argument('art__summary',
                         required=True,
                         help="The summary field is required")

    parser.add_argument('art__image',
                         required=True,
                         help="The image field is required")

    parser.add_argument('art__tags',
                         required=True,
                         help="The tags field is required")

    def get(self,param):
        p = PostModel.find_by_id(int(param))
        
        if p:
            x = {}
            x['log'] = p.json()
            post = p.get_post()
            x['post'] = post.json()
            x['post']['tags'] = post.get_tags()

            return {"error":0,"content":x}
        else :
            return {"error": 1 }


    def post(self, param):

        data = AdminProduct.parser.parse_args()

        try :
            product = ProductModel(
                data.art__title,
                data.art__author,
                data.art__body,
                data.art__summary,
                data.art__image)

            product.save()

            post = PostModel(product.id, 1)
            post.save()

            image = RepoFileModel.find_by_id(data.art__image)
            image.increase_users()

            for tag in data.art__tags:
                newTag = ProductTagModel(product.id, tag)
                newTag.save()
           
            return {"error": 0}
        except:
            return {"error": 1}


    def put(self,param):
        data = AdminProduct.parser.parse_args()

        product = ProductModel.find_by_id(param)

        if bool(product):
            if product.imageId != data.art__image:
                product.image.decrease_users()
                image = RepoFileModel.find_by_id(data.art__image)
                image.increase_users()

            product.title = data.art__title
            product.author = data.art__author
            product.body = data.art__body
            product.summary = data.art__summary
            product.imageId = data.art__image
            product.save()

            ProductTagModel.update_tags(product.id, json.loads(data.art__tags))


            try:
                
                return {"error": 0}
            except:
                return {"error": 2}
        else :
            return {"error": 1 ,"error_msg":"Product doesn't exist!"}

