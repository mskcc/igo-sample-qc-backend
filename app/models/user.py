import datetime
from app import db
# from flask_sqlalchemy import event
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import ldap


# three roles:
# igo_user: can view their projects
# member: can see all projects
# super: can promote
# supers = [
#     'bourquec',
#     'vialea',
#     'wagnerl',
#     'zimelc',

# ]
# members = [
#     'cavatorm',
#     'sunl',
#     'wenrichr',
#     'youd',

# ]

# ldap config to allow communication between this app and MSK LDAP server
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)


def get_ldap_connection():
    conn = ldap.initialize('ldaps://ldapha.mskcc.root.mskcc.org/')
    conn.set_option(ldap.OPT_REFERRALS, 0)
    return conn


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(40), nullable=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    title = db.Column(db.String(40), nullable=True)
    role = db.Column(db.String(40), nullable=True)
    children = relationship("Comment")

    def __init__(self, username, full_name=None, title=None, role='user'):

        self.username = username
        self.title = title
        self.full_name = full_name
        self.role = role
        self.full_name = full_name

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'username': self.username,
            'title': self.title,
            'full_name': self.full_name,
            'role': self.role,
        }

    # if you call this from the view (like, User.login(username, password) it will pass the credentials
    # on to LDAP and return either the result containing all the user's groups or a LDAP exception
    # that will be caught in the view

    @staticmethod
    def try_login(username, password):
        conn = get_ldap_connection()

        conn.simple_bind_s('%s@mskcc.org' % username, password)
        # attrs = ['memberOf']
        attrs = ['sAMAccountName', 'displayName', 'memberOf', 'title']
        # get the groups the user is a part of
        result = conn.search_s(
            'DC=MSKCC,DC=ROOT,DC=MSKCC,DC=ORG',
            ldap.SCOPE_SUBTREE,
            'sAMAccountName=' + username,
            attrs,
        )
        # if you want to see what comes back in the terminal
        # print(result)

        conn.unbind_s()
        return result


# def insert_initial_values(*args, **kwargs):
#     for user in supers:
#         db.session.add(User(username=user, role='super'))
#     for user in members:
#         db.session.add(User(username=user, role='member'))
#     db.session.commit()


# event.listen(User.__table__, 'after_create', insert_initial_values)
