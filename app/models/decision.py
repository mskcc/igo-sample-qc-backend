import datetime
from app import db


# Model to define decisions
class Decision(db.Model):

    __tablename__ = "decisions"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(40), nullable=False)
    decision_maker = db.Column(db.String(40), db.ForeignKey('users.username'))
    comment_relation_id = db.Column(db.Integer, db.ForeignKey('commentrelations.id'))
    report = db.Column(db.String(40), nullable=False)
    decisions = db.Column(db.Text(4294000000), nullable=False)
    is_igo_decision = db.Column(db.Boolean(), nullable=False)
    is_submitted = db.Column(db.Boolean(), nullable=False)
    date_created = db.Column(db.DateTime, nullable=True)
    date_updated = db.Column(db.DateTime, nullable=True)

    def __init__(
        self,
        request_id,
        report,
        decisions,
        date_updated,
        is_igo_decision=False,
        is_submitted=False,
        date_created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ):

        self.request_id = request_id
        self.report = report
        self.decisions = decisions
        self.is_igo_decision = is_igo_decision
        self.is_submitted = is_submitted
        self.date_created = date_created
        self.date_updated = date_updated

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "request_id": self.request_id,
            "report": self.report,
            "decisions": self.decisions,
            "is_igo_decision": self.is_igo_decision,
            "is_submitted": self.is_submitted,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "date_updated": self.date_updated.strftime("%Y-%m-%d %H:%M:%S"),
        }
