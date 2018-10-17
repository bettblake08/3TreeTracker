""" This module hosts the repo file api resource. """
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from app.database.models import RepoFileModel


class RepoFile(Resource):
    """ This class is the repo file api resource. """
    def get(self, file_id):
        """ Soft Delete Repo File Endpoint
        :args
            file_id : Id of repo file
        """
        repo_file = RepoFileModel.find_by_id(file_id)

        if not repo_file:
            return {
                "message": "Repo file does not exist!"
            }, 404

        used = repo_file.check_if_used()

        if used:
            return {
                "message": "Repo file is currently being used!"
            }, 403

        try:
            repo_file.delete()
            return {
                "message": "You have successfully deleted the repo file!"
            }, 200
            
        except:
            return {
                "message": "Failed to delete repo file!"
            }, 500


    def delete(self, file_id):
        """ Hard Delete Repo File Endpoint
        :args
            file_id : Id of repo file
        """
        repo_file = RepoFileModel.find_by_id(file_id)

        if not repo_file:
            return {
                "message": "Repo file does not exist!"
            }, 404
        
        try:
            repo_file.delete()

            return {
                "message": "You have successfully deleted the repo file!"
            }, 200

        except:
            return {
                "message": "Failed to delete repo file!"
            }, 500
