""" This module hosts the post api resource. """
from flask_restful import Resource

from app.database.models import PostModel


class Post(Resource):
    """ This class is the post api resource """
    def delete(self, param):
        """ Delete Post Endpoint """
        post = PostModel.find_by_id(param)

        if not post:
            return {
                "message": "Post does not exist!"
            }, 404

        try :
            post.delete()
            return {
                "message": "You have successfully deleted the post!"
                }, 200
            
        except :
            return {
                "message": "Failed to delete post!"
                }, 500           
