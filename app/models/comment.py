import datetime
from app import db
# import User



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


# @property
#   def serialize(self):
#       """Return object data in easily serializable format"""
#       return {
#           'id': self.id,
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
