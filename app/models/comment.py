import datetime
from app import db

# Model
class Comment(db.Model):
    """
    Create a Comment table
    """

    __tablename__ = "comments"
    # __table_args__ = ??

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    user_title = db.Column(db.String(60), nullable=False)
    comment = db.Column(db.Text(), nullable=False)
    request_id = db.Column(db.String(40), nullable=False)
    qc_table = db.Column(db.String(40), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    date_updated = db.Column(db.DateTime, nullable=True)

    def __init__(
        self,
        username,
        user_title,
        comment,
        request_id,
        qc_table,
        date_updated,
        date_created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ):

        self.username = username
        self.user_title = user_title
        self.comment = comment
        self.request_id = request_id
        self.qc_table = qc_table
        self.date_created = date_created
        self.date_updated = date_updated

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "username": self.username,
            "user_title": self.user_title,
            "comment": self.comment,
            "request_id": self.request_id,
            "qc_table": self.qc_table,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "date_updated": self.date_updated.strftime("%Y-%m-%d %H:%M:%S"),
        }


# @property
#   def serialize(self):
#       """Return object data in easily serializable format"""
#       return {
#           'id': self.id,
#           'username': self.username,
#           'version': self.version,
#           'service_id': self.service_id,
#           'transaction_id': self.transaction_id,
#           'material': self.material,
#           'application': self.application,
#           'form_values': self.form_values,
#           'grid_values': self.grid_values,
#           'submitted': self.submitted,
#           'created_on': self.created_on.strftime('%Y-%m-%d %H:%M:%S'),
#           'submitted_on': self.submitted_on.strftime('%Y-%m-%d %H:%M:%S') if self.submitted_on else None,
#       }
