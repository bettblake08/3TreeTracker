import datetime
import shutil

from app.database.db import DATABASE


class ProductTagModel(DATABASE.Model):
    __tablename__ = "product_tags"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    productId = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("products.id"))
    tagId = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('tags.id'))

    product = DATABASE.relationship('ProductModel')
    tag = DATABASE.relationship('TagModel')

    def __init__(self, productId, tagId):
        self.productId = productId
        self.tagId = tagId

    def json(self):
        return {"id": self.id, "tagId": self.tagId}

    def get_tag_name(self):
        return self.tag.json()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter(id=_id).first()

    @classmethod
    def update_tags(cls, productId, updatedTags):
        try:
            tags = cls.query.filter_by(productId=productId)
            s = [t.tagId for t in tags]

            for tag in tags:
                if tag.tagId not in updatedTags:
                    tag.delete()

            for x in updatedTags:
                if x not in s:
                    newTag = ProductTagModel(productId, x)
                    newTag.save()

            return True
        except:
            return False

    @classmethod
    def delete_all_product_tags(cls, productId):
        try:
            tags = cls.query.filter_by(productId=productId)

            for tag in tags:
                tag.delete()

            return True
        except:
            return False

    def save(self):
        DATABASE.session.add(self)
        DATABASE.session.commit()

    def delete(self):
        DATABASE.session.delete(self)
        DATABASE.session.commit()
