import datetime
import json

from flask import jsonify
from sqlalchemy import or_
from werkzeug.security import check_password_hash

from app.database.db import DATABASE


class LongrichUserModel(DATABASE.Model):
    __tablename__ = "accounts"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    name = DATABASE.Column(DATABASE.String(30))
    surname = DATABASE.Column(DATABASE.String(30))
    email = DATABASE.Column(DATABASE.String(30))
    phoneNo = DATABASE.Column(DATABASE.String(20))
    gender = DATABASE.Column(DATABASE.Integer)
    nationality = DATABASE.Column(DATABASE.String(3))
    placementId = DATABASE.Column(DATABASE.Integer)
    parentId = DATABASE.Column(DATABASE.Integer)
    verified = DATABASE.Column(DATABASE.Boolean)
    code = DATABASE.Column(DATABASE.String(20))
    password = DATABASE.Column(DATABASE.String(160))
    downliners = DATABASE.Column(DATABASE.String(60))
    created_at = DATABASE.Column(DATABASE.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, **params):
        self.name = params["name"]
        self.surname = params["surname"]
        self.email = params["email"]
        self.phoneNo = params["phoneNo"]
        self.gender = params["gender"]
        self.nationality = params["nationality"]
        self.placementId = params["placement"]
        self.verified = False
        self.code = ""
        self.parentId = 0
        self.password = params["password"]
        self.downliners = json.dumps([])

    def json(self):
        return {
            "id": self.id,
            "surname": self.surname,
            "name": self.name,
            "email": self.email,
            "phoneNo": self.phoneNo,
            "gender": self.gender,
            "nationality": self.nationality,
            "placementId": self.placementId,
            "verified": self.verified,
            "code": self.code
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(or_(LongrichUserModel.name.like("%" + name + "%"), LongrichUserModel.surname.like("%" + name + "%"))).filter(cls.verified == True)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    @classmethod
    def get_placements(cls, placements):
        return cls.query.filter(cls.id.in_(placements))

    @classmethod
    def get_users_by_offset(cls, name, country, offset):
        if name == "0":
            name = ""

        if country == "0":
            country = ""

        return cls.query.filter(or_(LongrichUserModel.name.like("%" + name + "%"), LongrichUserModel.surname.like("%" + name + "%"))).filter(cls.nationality.like("%" + country + "%")).order_by(cls.created_at).offset(offset).limit(50).all()

    @classmethod
    def find_placement(cls, placementId):
        users = [placementId]

        for u in users:
            user = cls.find_by_id(u)

            if user:
                downliners = json.loads(user.downliners)
                if len(downliners) >= 3:
                    for d in downliners:
                        users.append(d)
                else:
                    return user

        return None

    def get_downliners(self):
        return self.query.filter(self.id.in_(json.load(self.downliners)))

    def set_downliner(self, _id):
        downliners = json.loads(self.downliners)
        downliners.append(_id)
        self.downliners = json.dumps(downliners)
        self.save()

    def get_placement(self):
        return self.query.get(self.placementId)

    def verify(self, code):
        if self.placementId != 0:
            user = LongrichUserModel.find_by_id(self.placementId)

            if user:
                user.set_downliner(self.id)

                self.verified = True
                self.code = code
                self.save()

                return True
            else:
                return False

        else:
            self.verified = True
            self.code = code
            self.save()

            return True

    def authenticate(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        DATABASE.session.add(self)
        DATABASE.session.commit()

    def delete(self):
        DATABASE.session.delete(self)
        DATABASE.session.commit()
