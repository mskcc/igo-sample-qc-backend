from flask import Flask, Blueprint, json, jsonify, request, make_response
import requests
from app import app


LIMS_API_ROOT = app.config["LIMS_API_ROOT"]
LIMS_USER = app.config["LIMS_USER"]
LIMS_PW = app.config["LIMS_PW"]

tree = Blueprint('tree', __name__)


s = requests.Session()
# s.mount("https://", MyAdapter())


# returns request level information including a list of samples in the request
@tree.route("/tree", methods=['GET'])
def tree_request_id():
    
    request_id = request.args.get("request_id")

    # the API endpoint
    r = s.get(
				LIMS_API_ROOT + "/LimsRest/api/getRequestSamples?request=" + request_id,
                auth=(LIMS_USER, LIMS_PW),
                verify=False,
            )
    # print(r.text)
    return r.text;
