from app.database.db import DATABASE
from werkzeug.security import check_password_hash


class UserModel(DATABASE.Model):
    __tablename__ = "users"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    user = DATABASE.Column(DATABASE.String(30))

    def __init__(self, user):
        self.user = user

    def json(self):
        return {"id": self.id, "user": self.user}

    @classmethod
    def find_by_user(cls, name):
        return cls.query.filter_by(user=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    def save(self):
        DATABASE.session.add(self)
        DATABASE.session.commit()

    def delete(self):
        DATABASE.session.delete(self)
        DATABASE.session.commit()
