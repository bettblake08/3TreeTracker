import datetime
from app.database.db import DATABASE


class ProductStatsModel(DATABASE.Model):
    __tablename__ = "product_stats"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    productId = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('products.id'))
    userId = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('users.id'))
    reaction = DATABASE.Column(DATABASE.Integer)
    seen = DATABASE.Column(DATABASE.Boolean)
    reactionSeen = DATABASE.Column(DATABASE.Boolean)
    created_at = DATABASE.Column(DATABASE.DateTime, default=datetime.datetime.utcnow())

    # Reaction
    #1 - Liked
    #2 - Disliked

    product = DATABASE.relationship('ProductModel')
    user = DATABASE.relationship('UserModel')

    def __init__(self, productId, userId):
        self.productId = productId
        self.userId = userId
        self.reaction = 0
        self.seen = False
        self.reactionSeen = False

    def json(self):
        return {
            "id": self.id,
            "user": self.userId,
            "reaction": self.reaction,
            "seen": self.seen,
            "reactionSeen": self.reactionSeen
        }

    @classmethod
    def find(cls, pid, userid):
        return cls.query.filter_by(productId=pid, userId=userid).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def find_by_product(cls, pid):
        return cls.query.filter_by(productId=pid)

    @classmethod
    def check_if_user_has_seen(cls, user, productId):
        stat = cls.query.filter(user=user, productId=productId).first()
        return bool(stat)

    @classmethod
    def delete_all_product_stats(cls, productId):
        try:
            stats = cls.query.filter_by(productId=productId)

            for s in stats:
                s.delete()

            return True
        except:
            return False

    def save(self):
        DATABASE.session.add(self)
        DATABASE.session.commit()

    def delete(self):
        DATABASE.session.delete(self)
        DATABASE.session.commit()
