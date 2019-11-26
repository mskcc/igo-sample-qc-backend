from app import app
from flask import request
import inspect
from flask_login import current_user


def log_lims(lims_response, username="anonymous"):
    msg = (
        "\n"
        + "\n---LIMS Request---\n"
        + "User: "
        + username
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


def log_info(msg, username="anonymous"):
    app.logger.info(format(msg, username, "Flask"))


def log_error(msg):
    app.logger.error(format(msg, username, "Flask"))


def format(msg, username, source):

    return (
        "\n---"
        + source
        + " Request---\n"
        + "Endpoint: "
        + str(request.path)
        + "\n"
        + "Function: "
        + inspect.stack()[3][3]
        + "\n"
        + "User: "
        + username
        + "\n"
        + "\n"
        + str(msg)
    )
