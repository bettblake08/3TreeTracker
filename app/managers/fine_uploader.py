import os
import shutil
import random

from app.database.models import RepoFileModel
from app.managers.image_manager import ImageManager
from instance.config import Config


class FineUploader:
    """ This class handles all the file upload functions required for the repo files"""
    BASE_DIR = os.path.dirname(__file__)

    MEDIA_ROOT = os.path.join(BASE_DIR, '../../' + Config.REPO_DIR)
    UPLOAD_DIRECTORY = os.path.join(MEDIA_ROOT, 'upload')
    CHUNKS_DIRECTORY = os.path.join(MEDIA_ROOT, 'chunks')

    @classmethod
    def handle_delete(cls, uuid):
        """ Handles a filesystem delete based on UUID."""
        location = os.path.join(cls.UPLOAD_DIRECTORY, uuid)
        shutil.rmtree(location)

    @classmethod
    def handle_file_delete(cls, current_file):
        """ Handles a filesystem delete based on UUID."""
        folder_path = os.path.join(
            cls.UPLOAD_DIRECTORY,
            "{}/".format(current_file.name)
        )

        shutil.rmtree(folder_path)

        file_path = os.path.join(
            cls.UPLOAD_DIRECTORY,
            "{}.{}".format(
                current_file.name,
                current_file.fileType
                )
            )

        os.remove(file_path)

    @classmethod
    def handle_upload(cls, upload_file, attrs):
        """ Handle a chunked or non-chunked upload.
        """

        if attrs['folderId'] == "root":
            folder_id = 0
        else:
            folder_id = attrs['folderId']

        chunked = False
        dest_folder = os.path.join(cls.UPLOAD_DIRECTORY, attrs['qquuid'])
        dest = os.path.join(dest_folder, attrs['qqfilename'])

        # Chunked
        if 'qqtotalparts' in attrs and int(attrs['qqtotalparts']) > 1:
            chunked = True
            dest_folder = os.path.join(
                cls.CHUNKS_DIRECTORY,
                attrs['qquuid'])

            dest = os.path.join(
                dest_folder,
                attrs['qqfilename'],
                str(attrs['qqpartindex']))

            cls.save_upload(upload_file, dest)
        else:
            # Generate repo file in database before saving actual file

            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMOPQRTUVWXYZ0123456789"
            file_name = "".join(random.sample(chars, 6))

            while RepoFileModel.exists(file_name):
                file_name = "".join(random.sample(chars, 6))

            og_name = attrs['qqfilename']
            original_name = og_name.split(".")

            new_file = RepoFileModel(
                file_name,
                original_name[0],
                original_name[1],
                folder_id,
                attrs['qquuid'])

            new_file.save()

            dest = os.path.join(
                cls.UPLOAD_DIRECTORY,
                file_name + "." + original_name[1]
            )
            cls.save_upload(upload_file, dest)

            ImageManager.create_thumbnails(new_file)
            # ^^^ Generate repo file in database before saving actual file

        if chunked and (int(attrs['qqtotalparts']) - 1 == int(attrs['qqpartindex'])):

            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMOPQRTUVWXYZ0123456789"
            file_name = "".join(random.sample(chars, 6))

            while RepoFileModel.exists(file_name):
                file_name = "".join(random.sample(chars, 6))

            og_name = attrs['qqfilename']
            original_name = og_name.split(".")

            new_file = RepoFileModel(
                file_name,
                original_name[0],
                original_name[1],
                folder_id,
                attrs['qquuid'])

            new_file.save()

            dst = os.path.join(
                cls.UPLOAD_DIRECTORY,
                file_name + "." + original_name[1])

            cls.combine_chunks(
                attrs['qqtotalparts'],
                attrs['qqtotalfilesize'],
                source_folder=os.path.dirname(dest),
                dest=dst)

            shutil.rmtree(os.path.dirname(os.path.dirname(dest)))

            ImageManager.create_thumbnails(new_file)

    @classmethod
    def save_upload(cls, upload_file, path):
        """ Save an upload.
        Uploads are stored in <REPO_DIR>/uploads
        """

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(path, 'wb+') as destination:
            destination.write(upload_file.read())

    @classmethod
    def combine_chunks(cls, total_parts, total_size, source_folder, dest):
        """ Combine a chunked file into a whole file again. Goes through each part
        , in order, and appends that part's bytes to another destination file.

        Chunks are stored in <REPO_DIR>/chunks
        Uploads are saved in <REPO_DIR>/uploads
        """

        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))

        with open(dest, 'wb+') as destination:
            for part in range(int(total_parts)):
                part = os.path.join(source_folder, str(part))
                with open(part, 'rb') as source:
                    destination.write(source.read())
