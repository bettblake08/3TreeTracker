import datetime

from app.database.models.product_comment_stats import ProductCommentStatModel
from app.database.models.user import UserModel
from app.database.db import DATABASE


class ProductCommentModel(DATABASE.Model):
    __tablename__ = "product_comments"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    productId = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('products.id'))
    userName = DATABASE.Column(DATABASE.String(60))
    userEmail = DATABASE.Column(DATABASE.String(60))
    comment = DATABASE.Column(DATABASE.String(5000))
    seen = DATABASE.Column(DATABASE.Boolean)
    created_at = DATABASE.Column(DATABASE.DateTime, default=datetime.datetime.utcnow)

    # Reaction
    #1 - Liked
    #2 - Disliked

    product = DATABASE.relationship('ProductModel')
    stats = []

    def __init__(self, productId, userName, userEmail, comment):
        self.productId = productId
        self.userName = userName
        self.userEmail = userEmail
        self.comment = comment
        self.seen = False

    def json(self):
        return {
            "id": self.id,
            "productId": self.productId,
            "userName": self.userName,
            "userEmail": self.userEmail,
            "comment": self.comment,
            "stats": [x.json() for x in self.stats],
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def get_comments(cls, id, offset):
        comments = cls.query.filter_by(productId=id).order_by(
            cls.created_at).offset(offset).limit(30).all()

        cstats = ProductCommentStatModel.find_by_comments(
            [x.id for x in comments])

        for c in comments:
            c.stats = []
            for s in cstats:
                if s.commentId == c.id:
                    c.stats.append(s)

        return comments

    def set_reaction(self, userid, reaction):

        try:
            user = UserModel.find_by_user(userid)

            if not user:
                user = UserModel(userid)
                user.save()
                stat = ProductCommentStatModel(self.id, user.id)

            else:
                stat = ProductCommentStatModel.find(self.id, user.id)

                if not stat:
                    stat = ProductCommentStatModel(self.id, user.id)

            stat.reaction = reaction
            stat.save()

            return True
        except:
            return False

    @classmethod
    def delete_all_comments(cls, productId):
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
        ProductCommentStatModel.delete_all_comment_stats(self.id)

        DATABASE.session.delete(self)
        DATABASE.session.commit()
