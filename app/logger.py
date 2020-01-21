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

    # app.logger.info(msg)


def log_info(msg):
    app.logger.info(format(msg))


def log_email(msg, username, type):
    
    app.logger.info((
        "\n"
        + "\n---"
        + type
        + " EMAIL SENT ---\n"
        + "ENDPOINT: "
        + str(request.path)
        + "\n"
        + str(msg)
    ))


def log_error(msg):
    app.logger.error(format(msg))


def format(msg):
    return (
        "\n"
        + "\n--- FLASK REQUEST---\n"
        + "ENDPOINT: "
        + str(request.path)
        + "\n"
        + str(msg)
    )
