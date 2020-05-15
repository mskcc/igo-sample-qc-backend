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
    author = db.Column(db.String(40), db.ForeignKey('users.username'))
    recipients = db.Column(db.Text(), nullable=False)
    is_cmo_pm_project = db.Column(db.Boolean(), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False)
    date_updated = db.Column(db.DateTime, nullable=True)
    children = relationship("Comment", order_by="Comment.date_created")
    decision = relationship("Decision")

    def __init__(
        self,
        request_id,
        report,
        recipients,
        date_updated,
        date_created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        is_cmo_pm_project=False,
    ):

        self.request_id = request_id
        self.report = report
        self.recipients = recipients
        self.is_cmo_pm_project = is_cmo_pm_project
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
            "is_cmo_pm_project": self.is_cmo_pm_project,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "date_updated": self.date_updated.strftime("%Y-%m-%d %H:%M:%S"),
        }
