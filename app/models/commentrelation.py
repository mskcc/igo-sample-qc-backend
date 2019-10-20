import datetime
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Model to define a comment's recipients and report
class CommentRelation(db.Model):

    __tablename__ = "commentrelations"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(40), nullable=False)
    report = db.Column(db.Text(), nullable=False)
    recipients = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    date_updated = db.Column(db.DateTime, nullable=True)
    children = relationship("Comment", order_by="Comment.date_created")

    def __init__(
        self,
        request_id,
        report,
        recipients,
        date_updated,
        date_created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ):

        self.request_id = request_id
        self.report = report
        self.recipients = recipients
        self.date_created = date_created
        self.date_updated = date_updated

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "request_id": self.request_id,
            "report": self.report,
            "recipients": self.recipients,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "date_updated": self.date_updated.strftime("%Y-%m-%d %H:%M:%S"),
        }
