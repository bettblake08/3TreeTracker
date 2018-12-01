import datetime
from app.database.db import DATABASE

class ProductCommentStatModel(DATABASE.Model):
    __tablename__ = "product_comment_stats"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    commentId = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('product_comments.id'))
    userId = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('users.id'))
    reaction = DATABASE.Column(DATABASE.Integer)
    created_at = DATABASE.Column(DATABASE.DateTime, default=datetime.datetime.utcnow())

    # Reaction
    #1 - Liked
    #2 - Disliked

    comment = DATABASE.relationship('ProductCommentModel')
    user = DATABASE.relationship('UserModel')

    def __init__(self, commentId, user):
        self.commentId = commentId
        self.userId = user
        self.reaction = 0

    def json(self):
        return {"id": self.id, "user": self.userId, "reaction": self.reaction}

    @classmethod
    def find(cls, cid, userid):
        return cls.query.filter_by(commentId=cid, userId=userid).first()

    @classmethod
    def find_by_comments(cls, comments):
        return cls.query.filter(cls.commentId.in_(comments)).all()

    @classmethod
    def delete_all_comment_stats(cls, commentId):
        try:
            stats = cls.query.filter_by(commentId=commentId)

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
