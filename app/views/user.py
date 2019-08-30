from flask import Flask, Blueprint, json, jsonify, request, make_response
from app import db
from app.models import User
# from sqlalchemy import update

# from datetime import datetime

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



# goes to User model/table and grabs everything in it
def load_users():
    users = User.query.all()
    users_response = []
    for x in users:
        users_response.append(x.serialize)
    return users_response


# goes to User model/table and grabs users of a specific role
def load_users_of_role(role):
    users = User.query.filter(
        User.role == role)
    users_response = []
    for x in users:
        users_response.append(x.serialize)
    return users_response