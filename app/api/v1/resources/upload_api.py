""" This module hosts the upload api resource."""
from flask import jsonify
from flask_restful import Resource, request

from app.managers.fine_uploader import FineUploader


class UploadAPI(Resource):
    """ View which will handle all upload requests sent by Fine Uploader.

    Handles POST and DELETE requests.
    """
    up = FineUploader()

    def post(self):
        """A POST request. Validate the form and then handle the upload
        based on the POSTed data. Does not handle extra parameters yet.
        """
        try:
            self.up.handle_upload(request.files['qqfile'], request.form)
            return {"success": True}, 200
        except:
            return {"success": False}, 400

    def delete(self, uuid):
        """A DELETE request. If found, deletes a file with the corresponding
        UUID from the server's filesystem.
        """
        try:
            self.up.handle_delete(uuid)
            return {"success": True}, 200

        except:
            return {"success": False}, 400
