
import datetime
from app import db
from flask_sqlalchemy import event


# three roles:
# igo_user: can view their projects
# member: can see all projects
# super: can promote
supers = [
    'bourquec',
    'vialea',
    'wagnerl',
    'zimelc',
    
]
members = [
    'cavatorm',
    'sunl',
    'wenrichr',
    'youd',

]


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(40), nullable=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    msk_group = db.Column(db.String(40), nullable=True)
    role = db.Column(db.String(40), nullable=True)

    def __init__(
        self, 
        username, 
        full_name=None, 
        msk_group=None, 
        role='user',
    ):

        self.username = username
        self.msk_group = msk_group
        self.role = role
        self.full_name = full_name

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'username': self.username,
            'msk_group': self.msk_group,
            'role': self.role,
        }


def insert_initial_values(*args, **kwargs):
    for user in supers:
        db.session.add(User(username=user, role='super'))
    for user in members:
        db.session.add(User(username=user, role='member'))
    db.session.commit()


event.listen(User.__table__, 'after_create', insert_initial_values)