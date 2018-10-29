""" This module hosts the tag api resource """
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from app.database.models import TagModel


class Tag(Resource):
    """ This class is the tag api resource. """
    def get(self, param):
        """ Post A New Tag Endpoint """
        
        if TagModel.exists(param):
            return {
                "message": "Tag already exists!"
            }, 403

        tag = TagModel(param)

        try:
            tag.save()
            return {
                "message": "You have successfully posted a new tag!",
                "content": tag.json()
                }, 201
        except:
            return {
                "message": "Failed to post a new tag!"
                }, 500

    def delete(self, param):
        new_tag = TagModel.find_by_id(param)

        if not new_tag:
            return {
                "message": "Tag does not exist!"
            }, 404

        try:
            new_tag.delete()
            return {
                "message": "You have successfully deleted the tag!"
            }, 200
        except:
            return {
                "message": "Failed to delete tag!"
            }, 500


class Tags(Resource):
    """ This class is the tags api resource """
    def get(self, param):
        """ Get Tags By Name Endpoint """

        try:
            tags = TagModel.search_by_name(param)
            return {
                "message": 0,
                "content": [tag.json() for tag in tags]
                }, 200
        except:
            return {
                "message": "Failed to retrieve tags!"
                }, 500
