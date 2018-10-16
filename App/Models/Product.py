from db import db
from App.Models.ProductTag import ProductTagModel
from App.Models.RepoFile import RepoFileModel
from App.Models.User import UserModel

from App.Models.ProductStats import ProductStatsModel

class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.String(60000))
    summary = db.Column(db.String(200))
    imageId = db.Column(db.Integer, db.ForeignKey("repo_file.id"))
    views = db.Column(db.Integer)
    reactions = db.Column(db.Integer)
    comments = db.Column(db.Integer)

    db.relationship('PostModel')
    image = db.relationship('RepoFileModel')
    tags = db.relationship('ProductTagModel')
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
            "stat":{
                "views":self.views,
                "reactions": self.reactions,
                "comments":self.comments
            },
            "stats":[x.json() for x in self.stats]
         }


    @classmethod
    def find_by_id(cls,_id):
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


    def set_reaction(self,userid,reaction):
           
        try :
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
        db.session.add(self)
        db.session.commit()


    def delete(self):
        ProductTagModel.delete_all_product_tags()
        image = RepoFileModel.find_by_id(self.imageId)
        image.decrease_user()
        
        db.session.delete(self)
        db.session.commit()
