import datetime
from app import db


# Model to define decisions
class Decision(db.Model):

    __tablename__ = "decisions"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(40), nullable=False)
    decision_maker = db.Column(db.String(40), db.ForeignKey('users.username'))
    comment_relation_id = db.Column(db.Integer, db.ForeignKey('commentrelations.id'))
    decisions = db.Column(db.Text(), nullable=False)
    date_updated = db.Column(db.DateTime, nullable=True)

    def __init__(
        self,
        request_id,
        decisions,
        date_updated,
        date_created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ):

        self.request_id = request_id
        self.decisions = decisions
        self.date_created = date_created
        self.date_updated = date_updated

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "request_id": self.request_id,
            "decisions": self.decisions,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "date_updated": self.date_updated.strftime("%Y-%m-%d %H:%M:%S"),
        }
