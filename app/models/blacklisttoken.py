from app import app, db


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """

    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))


    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def is_jti_blacklisted(jti):
        query = BlacklistToken.query.filter_by(jti=jti).first()
        return bool(query)
