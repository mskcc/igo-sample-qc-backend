from app import app
from flask import request
import inspect
from flask_login import current_user

def log_lims(lims_response):
    msg = (
        "\n"
        + "\n---LIMS Request---\n"
        + "User: " + str(current_user.username if current_user.username else "anynymous")
        + "\n"
        + 'Endpoint: '
        + str(lims_response.url)
        + "\nStatus code: "
        + str(lims_response.status_code)
        + "\n"
        + "Data: "
        + lims_response.text
        + "\n"
    )
    app.logger.info(msg)


def log_info(msg):
    app.logger.info(format(msg, "Flask") )


def log_error(msg):   
    app.logger.error(format(msg, "Flask"))


def format(msg, source):
    
    return (
        "\n---"
        + source 
        + " Request---\n"
        + "Endpoint: "
        + str(request.path)
        + "\n"
        + "Function: "
        + inspect.stack()[2][3]
        + "\n"
        + str(msg)
        
    )
