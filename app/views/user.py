from flask import Flask, Blueprint, json, jsonify, request, make_response
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    get_raw_jwt,
    create_access_token,
    jwt_refresh_token_required,
    create_refresh_token,
    get_jwt_identity,
)
from app import db, jwt
from app.models import User, BlacklistToken

# from sqlalchemy import update
import datetime
import re

# Might be necessary:
import ldap


# initializes user blueprint as an extension of the application
user = Blueprint('user', __name__)


# accepts a role argument and returns applicable users
@user.route("/getUsers", methods=['GET'])
def get_users():

    role = request.args.get("role")
    users_response = load_users_of_role(role)
    # columnDefs.append(copy.deepcopy(possible_fields[column[0]]))
    responseObject = {'users': users_response}

    return make_response(jsonify(responseObject), 200, None)


# login route
@user.route('/login', methods=['POST'])
def login():
    try:
        # gets the login data used
        try:
            payload = request.get_json()['data']
            username = payload["username"]
            password = payload["password"]
            # print(payload)

        # catches missing parameters
        except:
            responseObject = {
                'message': 'Missing username or password. Please try again.'
            }
            return make_response(jsonify(responseObject), 401, None)
        # tries logging in
        try:
            result = User.try_login(username, password)
        # catches invalid credentials from LDAP call in user model
        except ldap.INVALID_CREDENTIALS:
            # log_error(
            # "user " + username + " trying to login with invalid credentials"
            # )
            responseObject = {
                'message': 'Invalid username or password. Please try again.'
            }
            return make_response(jsonify(responseObject), 401, None)
        # if the user is part of GRP_SKI_Haystack_NetIQ
        if is_authorized(result):
            # log_info('authorized user loaded: ' + username)

            # Ignore for now, this is to load the user from the table or create a new one
            user = load_username(username)

            # Create our JWTs
            # default expiration 15 minutes
            access_token = create_access_token(identity=username)

            # default expiration 30 days, changed to 12 hours
            expires = datetime.timedelta(hours=12)
            refresh_token = create_refresh_token(
                identity=username, expires_delta=expires
            )

            responseObject = {
                'status': 'success',
                'message': 'Hello, ' + username + '. You have successfully logged in.',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'username': user.username,
                # 'userTitle': user.title,
            }
            return make_response(jsonify(responseObject), 200, None)
        else:
            # log_error(
            #     "user "
            #     + username
            #     + " AD authenticated but not in GRP_SKI_Haystack_NetIQ"
            # )
            return make_response(
                'You are not authorized to view this website. Please email <a href="mailto:wagnerl@mkscc.org">sample intake support</a> if you need any assistance.',
                403,
                None,
            )
    # catches all block in case anything unexpected goes wrong
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Our backend is experiencing some issues, please try again later or email an admin.',
        }
        return make_response(jsonify(responseObject)), 500


@user.route('/logoutAccess')
@jwt_required
def logoutAccess():
    jti = get_raw_jwt()['jti']
    try:
        revoked_token = BlacklistToken(jti=jti)
        revoked_token.add()
        responseObject = {
            'status': 'success',
            'message': 'Access token has been revoked',
        }
        return make_response(jsonify(responseObject)), 200

    except Exception as e:
        responseObject = {'status': 'fail', 'message': e}
        return make_response(jsonify(responseObject)), 200


@user.route('/logoutRefresh', methods=['GET'])
@jwt_refresh_token_required
def logoutRefresh():
    jti = get_raw_jwt()['jti']
    try:
        revoked_token = BlacklistToken(jti=jti)
        revoked_token.add()
        responseObject = {
            'status': 'success',
            'message': 'Refresh token has been revoked',
        }
        return make_response(jsonify(responseObject)), 200

    except Exception as e:
        responseObject = {'status': 'fail', 'message': e}
        return make_response(jsonify(responseObject)), 200


# goes to User model/table and grabs everything in it
def load_users():
    users = User.query.all()
    users_response = []
    for x in users:
        users_response.append(x.serialize)
    return users_response


# goes to User model/table and grabs users of a specific role
def load_users_of_role(role):
    users = User.query.filter(User.role == role)
    users_response = []
    for x in users:
        users_response.append(x.serialize)
    return users_response


def load_username(username):
    return User.query.filter_by(username=username).first()


# checks whether user is in GRP_SKI_Haystack_NetIQ
def is_authorized(result):
    return "GRP_SKI_Haystack_NetIQ" in format_result(result)


# returns groups the user is a part of
def format_result(result):
    # compiles reg ex pattern into reg ex object
    p = re.compile('CN=(.*?)\,')
    groups = re.sub('CN=Users', '', str(result))
    # returns all matching groups
    return p.findall(groups)
