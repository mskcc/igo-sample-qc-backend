from flask import Flask, Blueprint, json, jsonify, request, make_response
import requests
from app import app


LIMS_API_ROOT = app.config["LIMS_API_ROOT"]
LIMS_USER = app.config["LIMS_USER"]
LIMS_PW = app.config["LIMS_PW"]

qcresult = Blueprint('qcresult', __name__)


# request = package.session
s = requests.Session()
# s.mount("https://", MyAdapter())

# three tables that will need to be connected in an endpoint? qcreportrna, dna, library
# suggestion: controller - getQCResult(request_id), service - getQCResult
@qcresult.route("/qcresult/rna")
def qcresult_rna():
    # the API endpoint 
    r = s.get(
                # LIMS_API_ROOT + "/LimsRest/getProjectQc?project='09938'",
                LIMS_API_ROOT + "/LimsRest/getPickListValues?list=Recipe",
                auth=(LIMS_USER, LIMS_PW),
                verify=False,
            )
    print(r.text)
    # return "rna-result";
    return r.text;
