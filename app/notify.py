from app import app, db, constants
from app.logger import log_info, log_error, log_lims

import traceback
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
from datetime import datetime

NOTIFICATION_SENDER = app.config["NOTIFICATION_SENDER"]
IGO_EMAIL = app.config["IGO_EMAIL"]
ENV = app.config["ENV"]


def send_decision_notification(decision, decision_user, recipients, initial_author):
    if ENV == 'development':

        recipients = [
            "wagnerl@mskcc.org",
            "patrunoa@mskcc.org",
            initial_author + "@mskcc.org",
        ]
        recipients = set(recipients)
    # receiver_email = recipients
    print(recipients, "send_decision_notification")
    sender_email = NOTIFICATION_SENDER
    # print(receiver_email.split(","))

    template = constants.decision_notification_email_template_html

    content = (
        template["body"] % (decision.request_id, decision_user.full_name)
        + template["footer"]
        # + "<br><br>In production, this email would have been sent to:"
        # + ", ".join(recipients)
    )
    msg = MIMEText(content, "html")
    msg['Subject'] = template["subject"] % (decision.request_id, decision.report)

    msg['From'] = sender_email
    msg['To'] = ', '.join(recipients)

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    # .sendmail(sender_email, receiver_email, message.as_string())
    # if ENV = development
    s.sendmail(sender_email, recipients, msg.as_string())
    s.close()
    log_info(msg.as_string(), decision_user.username)
    return "done"


def send_initial_notification(recipients, request_id, report, author):
    if ENV == 'development':

        recipients = [
            "wagnerl@mskcc.org",
            "patrunoa@mskcc.org",
            author.username + "@mskcc.org",
        ]
        recipients = set(recipients)

    print(recipients, "send_initial_notification")
    # receiver_email = recipients
    sender_email = NOTIFICATION_SENDER
    # print(receiver_email.split(","))

    template = constants.initial_email_template_html
    name = author.full_name
    content = template["body"] % (report.split(' ')[0], request_id) + template[
        "footer"
    ] % (name, author.title)
    msg = MIMEText(content, "html")
    msg['Subject'] = template["subject"] % request_id

    msg['From'] = sender_email
    msg['To'] = ", ".join(recipients)

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    # .sendmail(sender_email, receiver_email, message.as_string())
    # if ENV = development
    # s.sendmail(sender_email, recipients, msg.as_string())
    s.close()
    print(msg.as_string())
    return "done"


def send_notification(recipients, comment, request_id, report, author):
    if ENV == 'development':

        recipients = [
            "wagnerl@mskcc.org",
            "patrunoa@mskcc.org",
            author.username + "@mskcc.org",
        ]
        recipients = set(recipients)

    # receiver_email = recipients
    sender_email = NOTIFICATION_SENDER
    # print(receiver_email.split(","))

    template = constants.notification_email_template_html
    print(recipients, "send_notification")
    # print(recipients)
    name = author.full_name

    content = (
        template["body"] % (report.split(' ')[0], request_id, comment["content"])
        + template["footer"] % (name, author.title)
        # + "<br><br>In production, this email would have been sent to:"
        # + ", ".join(recipients)
    )
    msg = MIMEText(content, "html")
    msg['Subject'] = template["subject"] % request_id

    msg['From'] = sender_email
    msg['To'] = ', '.join(recipients)

    # # # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    # .sendmail(sender_email, receiver_email, message.as_string())
    # if ENV = development
    s.sendmail(sender_email, recipients, msg.as_string())
    s.close()
    print(msg)
    return "done"


def send_feedback(recipients, body, subject, type):
    receiver_email = recipients
    sender_email = NOTIFICATION_SENDER

    msg = MIMEText(body)
    msg['Subject'] = "New Feedback for Sample QC! " + type + " " + subject

    msg['From'] = sender_email
    msg['To'] = receiver_email
    s = smtplib.SMTP('localhost')
    s.sendmail(sender_email, receiver_email.split(","), msg.as_string())
    s.close()
    print(msg.as_string())
    return "done"
