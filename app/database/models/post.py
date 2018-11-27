import datetime
from app.database.db import DATABASE
from app.database.models.product import ProductModel

class PostModel(DATABASE.Model):
    __tablename__ = "posts"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    postId = DATABASE.Column(DATABASE.Integer)
    postType = DATABASE.Column(DATABASE.Integer)
    created_at = DATABASE.Column(DATABASE.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, postId, postType):
        self.postId = postId
        self.postType = postType

    def json(self):
        return {
            "id": self.id,
            "postId": self.postId,
            "type": self.postType,
            "created_at": str(self.created_at)
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def exists(cls, name):
        file = cls.query.filter_by(name=name).first()
        return bool(file)

    @classmethod
    def get_posts_by_offset(cls, offset):
        return cls.query.order_by(cls.created_at).offset(offset).limit(15).all()

    def get_post(self):
        if self.postType == 1:
            return ProductModel.find_by_id(self.postId)

    def save(self):
        DATABASE.session.add(self)
        DATABASE.session.commit()

    def delete(self):

        if self.postType == 1:
            product = ProductModel.find_by_id(self.postId)

            if product:
                product.delete()

        DATABASE.session.delete(self)
        DATABASE.session.commit()
