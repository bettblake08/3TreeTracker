from app.database.db import DATABASE


class RevokedTokenModel(DATABASE.Model):
    __tablename__ = 'expired_tokens'
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    token = DATABASE.Column(DATABASE.String(120))

    def __init__(self, token):
        self.token = token

    def save(self):
        DATABASE.session.add(self)
        DATABASE.session.commit()

    @classmethod
    def is_token_blacklisted(cls, jti):
        query = cls.query.filter_by(token=jti).first()
        return bool(query)
