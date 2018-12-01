from app.database.db import DATABASE
from app.database.models.product_tag import ProductTagModel
from app.database.models.repo_file import RepoFileModel
from app.database.models.user import UserModel
from app.database.models.product_stats import ProductStatsModel


class ProductModel(DATABASE.Model):
    __tablename__ = "products"

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    title = DATABASE.Column(DATABASE.String(80))
    body = DATABASE.Column(DATABASE.Text)
    summary = DATABASE.Column(DATABASE.String(200))
    imageId = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("repo_file.id"))
    views = DATABASE.Column(DATABASE.Integer)
    reactions = DATABASE.Column(DATABASE.Integer)
    comments = DATABASE.Column(DATABASE.Integer)

    DATABASE.relationship('PostModel')
    image = DATABASE.relationship('RepoFileModel')
    tags = DATABASE.relationship('ProductTagModel')
    stats = []

    def __init__(self, title, body, summary, imageId):
        self.title = title
        self.body = body
        self.summary = summary
        self.imageId = imageId
        self.views = 0
        self.reactions = 0
        self.comments = 0

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "summary": self.summary,
            'image': self.image.json(),
            "stat": {
                "views": self.views,
                "reactions": self.reactions,
                "comments": self.comments
            },
            "stats": [x.json() for x in self.stats]
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    def get_tags(self):
        return [x.get_tag_name() for x in self.tags]

    def get_stats(self):
        self.stats = ProductStatsModel.find_by_product(self.id)

    def set_visitor(self, userid):
        try:
            user = UserModel.find_by_user(userid)

            if not user:
                user = UserModel(userid)
                user.save()

            else:
                stat = ProductStatsModel.find(self.id, user.id)

                if stat:
                    return False            # Visitor to post has already been registered

            stat = ProductStatsModel(self.id, user.id)

            stat.save()
            self.views += 1
            self.save()

            return True
        except:
            return False

    def set_reaction(self, userid, reaction):

        try:
            user = UserModel.find_by_user(userid)

            if not user:
                user = UserModel(userid)
                user.save()
                stat = ProductStatsModel(self.id, user.id)

            else:
                stat = ProductStatsModel.find(self.id, user.id)

                if not stat:
                    stat = ProductStatsModel(self.id, user.id)

            stat.reaction = reaction
            stat.save()

            self.reactions += 1
            self.save()

            return True
        except:
            return False

    def save(self):
        DATABASE.session.add(self)
        DATABASE.session.commit()

    def delete(self):
        ProductTagModel.delete_all_product_tags()
        image = RepoFileModel.find_by_id(self.imageId)
        image.decrease_user()

        DATABASE.session.delete(self)
        DATABASE.session.commit()
