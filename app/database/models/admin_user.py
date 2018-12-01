from app.database.db import DATABASE
from werkzeug.security import check_password_hash


class AdminUserModel(DATABASE.Model):
    __tablename__ = "admin_user"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    username = DATABASE.Column(DATABASE.String(16))
    password = DATABASE.Column(DATABASE.String(160))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {"id": self.id, "username": self.username}

    @classmethod
    def find_by_username(cls, name):
        return cls.query.filter_by(username=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter(id=_id).first()

    def authenticate(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        DATABASE.session.add(self)
        DATABASE.session.commit()

    def delete(self):
        DATABASE.session.delete(self)
        DATABASE.session.commit()
