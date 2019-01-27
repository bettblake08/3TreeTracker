import os

from faker import Faker
from PIL import Image

from app.database.models import RepoFileModel
from app.managers.fine_uploader import FineUploader
from app.managers.image_manager import ImageManager
from instance.config import Config

BASE_DIR = os.path.dirname(__file__)
IMAGE_DIRECTORY = os.path.join(
    BASE_DIR,
    '../../../assets/images/'
)

UPLOAD_DIR = os.path.join(BASE_DIR, "../../../{}upload/".format(Config.REPO_DIR))

def generate_repo_file():
    """ This function handles the generation of repo files. """
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(os.path.dirname(UPLOAD_DIR))

    files = [
        {
            "name": "G67S5A",
            "ogName": "test",
            "fileType": "jpg",
            "folderId": 1,
            "uuid": "11aa"
        },
        {
            "name": "A67S5A",
            "ogName": "new_file",
            "fileType": "jpg",
            "folderId": 1,
            "uuid": "22aa"
        },
        {
            "name": "F67S5A",
            "ogName": "upload",
            "fileType": "jpg",
            "folderId": 1,
            "uuid": "33aa"
        }
    ]

    for ufile in files:
        new_file = RepoFileModel(
            ufile['name'],
            ufile['ogName'],
            ufile['fileType'],
            ufile['folderId'],
            ufile['uuid'])

        new_file.save()

        file_path = os.path.join(
            UPLOAD_DIR,
            "{}.{}".format(
                new_file.name,
                new_file.fileType
            )
        )

        if not os.path.exists(file_path):
            image = Image.open(IMAGE_DIRECTORY + "back--11.jpg")
            image.save(file_path)

            ImageManager.create_thumbnails(new_file)

def teardown_repo_file():
    files = RepoFileModel.query.all()

    for repo_file in files:
        FineUploader.handle_file_delete(repo_file)
