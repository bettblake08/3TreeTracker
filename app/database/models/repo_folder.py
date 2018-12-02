from app.database.db import DATABASE
from app.database.models.repo_file import RepoFileModel


class RepoFolderModel(DATABASE.Model):
    __tablename__ = "repo_folder"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    name = DATABASE.Column(DATABASE.String(60))
    parent = DATABASE.Column(DATABASE.Integer)

    files = DATABASE.relationship('RepoFileModel', lazy="dynamic")

    def __init__(self, name):
        self.name = name if name else ""

    def json(self):
        return {"id": self.id, "name": self.name}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def exists(cls, name, parent):
        file = cls.query.filter_by(name=name, parent=parent).first()
        return bool(file)

    def get_content(self, folderId):
        files = self.files.all()
        folders = self.query.filter_by(parent=folderId)

        resp = {
            "files": [x.json() for x in files],
            "folders": [x.json() for x in folders]
        }

        return resp

    @classmethod
    def get_root_content(cls):
        files = RepoFileModel.get_files_by_folder(0)
        folders = cls.query.filter_by(parent=0)

        resp = {
            "files": [x.json() for x in files],
            "folders": [x.json() for x in folders]
        }

        return resp

    def check_if_contains_content(self, _id):
        files = self.files.all()

        if len(files) > 0:
            return True

        folders = self.query.filter_by(parent=_id).first()
        return bool(folders)

    def save(self):
        DATABASE.session.add(self)
        DATABASE.session.commit()

    def delete(self):
        files = self.files.all()

        for x in files:
            x.delete()

        folders = self.query.filter_by(parent=self.id)

        for x in folders:
            x.delete()

        DATABASE.session.delete(self)
        DATABASE.session.commit()
