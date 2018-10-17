""" This module hosts the repo folder api resource. """
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from app.database.models import RepoFolderModel


class RepoFolder(Resource):
    """ This class is the repo folder api resource. """
    def post(self, param):
        """ Post A New Repo Folder Endpoint"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            "parentId",
            required=True,
            help="A parent folder id is required"
            )

        parser.add_argument(
            "name",
            required=True,
            help="A name is required"
            )

        data = parser.parse_args()
        if RepoFolderModel.exists(data.name, data.parentId):
            return {
                "message":"Folder already exists!"
                }, 403

        new_folder = RepoFolderModel()
        new_folder.name = data.name

        if data.parentId == "root":
            data.parentId = 1

        new_folder.parent = data.parentId

        try:
            new_folder.save()
            return {
                "message": "You have successfully created a new repo folder!"
            }, 201

        except:
            return {
                "message": "Failed to create a new repo folder!"
            }, 500


    def put(self, param):
        """ Update Repo Folder Endpoint
        :args
            param:  Repo folder id
        """
        parser = reqparse.RequestParser()

        parser.add_argument(
            "name",
            required=True,
            help="A folder name is required"
            )

        data = parser.parse_args()

        try:
            folder_id = int(param)
        except:
            return {
                "message": "Invalid repo folder id!"
            }, 400

        folder = RepoFolderModel.find_by_id(folder_id)

        if not folder:
            return {
                "message": "Folder does not exist!"
            }, 404

        folder.name = data.name

        try:
            folder.save()
            return {
                "message": "You have successfully updated the repo folder!"
            }, 200
        except:
            return {
                "message": "Failed to update the repo folder!"
            }, 500


    def get(self, param):
        """ Soft Delete Repo Folder Endpoint """

        try:
            folder_id = int(param)
        except:
            return {
                "message": "Invalid repo folder id!"
            }, 400
        
        folder = RepoFolderModel.find_by_id(folder_id)

        if not folder:
            return {
                "message": "Folder does not exist!"
            }, 404

        occupied = folder.check_if_contains_content(folder_id)

        if occupied:
            return {
                "message": "Folder contains files and/or folders!"
            }, 403
        
        try:
            folder.delete()
        except:
            return {
                "message": "Failed to delete repo folder!"
            }

    def delete(self, param):
        """ Hard Delete Repo Folder Endpoint """

        try:
            folder_id = int(param)
        except:
            return {
                "message": "Invalid repo folder id!"
            }, 400

        folder = RepoFolderModel.find_by_id(folder_id)

        if not folder:
            return {
                "message": "Folder does not exist!"
            }
        
        try:
            folder.delete()
            return {
                "message": "You have successfully deleted the repo folder!"
            }
        except:
            return {
                "message": "Failed to delete repo folder!"
            }, 500
