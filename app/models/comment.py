import datetime
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Model, parent of comment_relation
class Comment(db.Model):
    """
    Create a Comment table
    """

    __tablename__ = "comments"
    # __table_args__ = ??

    id = db.Column(db.Integer, primary_key=True)
    commentrelation_id = db.Column(db.Integer, db.ForeignKey('commentrelations.id'))
    username = db.Column(db.String(40), db.ForeignKey('users.username'))
    comment = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    date_updated = db.Column(db.DateTime, nullable=True)
    author = relationship("User")


    def __init__(
        self,
        comment,
        date_updated,
        date_created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ):

        self.comment = comment
        self.date_created = date_created
        self.date_updated = date_updated

    @property
    def serialize(self):
        # user = User.query.filter_by(username=self.username).first()
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "comment": self.comment,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "date_updated": self.date_updated.strftime("%Y-%m-%d %H:%M:%S"),
        }
