from app import app, db, constants
from app.logger import log_email, log_error, log_lims

import traceback
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
from datetime import datetime

from secret_config import TEST_EMAIL, WATCHER

# NOTIFICATION MODULE
# notifications are sent to recipients selected in initial report editor,
# editor is pre-filled with request level email information
# cmo_igo is pulled from recipients and bcc'd
NOTIFICATION_SENDER = app.config["NOTIFICATION_SENDER"]
IGO_EMAIL = app.config["IGO_EMAIL"]
IGO_BILLER = app.config["IGO_BILLER"]
ENV = app.config["ENV"]


def send_initial_notification(
    recipients, request_id, report, author, is_decided, is_pathology_report, is_covid_report, is_cmo_pm_project
):
    template = constants.initial_email_template_html
    if is_covid_report:
        body = template["covid_body"] % (report.split(' ')[0], request_id, request_id, request_id) 
    elif is_cmo_pm_project == True:
        body = template["cmo_pm_body"] % (report.split(' ')[0], request_id, request_id, request_id)
    else:
        body = template["body"] % (report.split(' ')[0], request_id, request_id, request_id) 
    if ENV == 'development':
        content = (
            body
            + template["footer"] % (author.full_name, author.title)
            + "<br><br>In production, this email would have been sent to:"
            + ", ".join(recipients)
            + "<br><br>"
            + str(constants.user_training_string)
        )
        recipients = [
            "delbels@mskcc.org",
            "mirhajf@mskcc.org",
            author.username + "@mskcc.org",
        ]
        recipients = set(recipients)
    else:
        content = (
            template["body"]
            % (report.split(' ')[0], request_id, request_id, request_id)
            + template["footer"] % (author.full_name, author.title)
            + "<br><br>"
            + str(constants.user_training_string)
        )

    msg = MIMEText(content, "html")

    if is_covid_report:
        msg['Subject'] = template["covid_subject"] % (request_id, report.split(' ')[0], "")
    elif is_decided or is_pathology_report or is_cmo_pm_project:
        msg['Subject'] = template["subject"] % (request_id, report.split(' ')[0], "")
    
    else:
        msg['Subject'] = template["subject"] % (
            request_id,
            report.split(' ')[0],
            ", Pending further action",
        )
    # print(recipients, "send_initial_notification")
    sender_email = NOTIFICATION_SENDER

    msg['From'] = sender_email
    all_recipients = recipients.copy()

    if IGO_EMAIL in recipients:
        recipients.discard(IGO_EMAIL)

    # the email header's "to" field is for display only, the actual to address is in the sendmail() params
    msg['To'] = ', '.join(recipients)

    # Send the message via our own SMTP server.

    s = smtplib.SMTP('localhost')
    s.sendmail(sender_email, all_recipients, msg.as_string())
    s.close()
    log_email(msg.as_string(), author.username, "Initial Comment")
    return "done"


def send_notification(recipients, comment, request_id, report, author):
    template = constants.notification_email_template_html

    if ENV == 'development':
        content = (
            template["body"]
            % (
                report.split(' ')[0],
                request_id,
                author.full_name,
                comment["content"],
                request_id,
                request_id,
            )
            + template["footer"]
            + "<br><br>In production, this email would have been sent to:"
            + ", ".join(recipients)
            + "<br><br>"
            + str(constants.user_training_string)
        )
        recipients = [
            "delbels@mskcc.org",
            "mirhajf@mskcc.org",
            author.username + "@mskcc.org",
        ]
        recipients = set(recipients)
    else:
        content = (
            template["body"]
            % (
                report.split(' ')[0],
                request_id,
                author.full_name,
                comment["content"],
                request_id,
                request_id,
            )
            + template["footer"]
            + "<br><br>"
            + str(constants.user_training_string)
        )
    sender_email = NOTIFICATION_SENDER
    # print(recipients, "send_notification")
    name = author.full_name

    msg = MIMEText(content, "html")
    msg['Subject'] = template["subject"] % request_id

    msg['From'] = sender_email
    all_recipients = recipients.copy()

    if IGO_EMAIL in recipients:
        recipients.discard(IGO_EMAIL)

    # the email header's "to" field is for display only, the actual to address is in the sendmail() params
    msg['To'] = ', '.join(recipients)
    # # # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.sendmail(sender_email, all_recipients, msg.as_string())
    s.close()
    log_email(msg.as_string(), author.username, "Additional Comment")
    return "done"


def send_decision_notification(decision, decision_user, recipients, initial_author):
    template = constants.decision_notification_email_template_html
    if ENV == 'development':
        content = (
            template["body"]
            % (
                decision.request_id,
                decision_user.full_name,
                decision.request_id,
                decision.request_id,
            )
            + template["footer"]
            + "<br><br>In production, this email would have been sent to:"
            + ", ".join(recipients)
            + "<br><br>"
            + str(constants.user_training_string)
        )
        recipients = [
            "delbels@mskcc.org",
            "mirhajf@mskcc.org",
            initial_author + "@mskcc.org",
        ]
        recipients = set(recipients)
    else:
        content = (
            template["body"]
            % (
                decision.request_id,
                decision_user.full_name,
                decision.request_id,
                decision.request_id,
            )
            + template["footer"]
            + "<br><br>"
            + str(constants.user_training_string)
        )
    # receiver_email = recipients
    # print(recipients, "send_decision_notification")
    sender_email = NOTIFICATION_SENDER
    # print(receiver_email.split(","))

    msg = MIMEText(content, "html")
    msg['Subject'] = template["subject"] % (decision.request_id, decision.report)

    msg['From'] = sender_email
    intial_author_email= initial_author + "@mskcc.org"
    recipients.add(intial_author_email)
    all_recipients = recipients.copy()

    if IGO_EMAIL in recipients:
        recipients.discard(IGO_EMAIL)

    # the email header's "to" field is for display only, the actual to address is in the sendmail() params
    msg['To'] = ', '.join(recipients)
    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.sendmail(sender_email, all_recipients, msg.as_string())
    s.close()
    log_email(msg.as_string(), decision_user.username, "Decision")
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
    log_email(msg.as_string(), "Feedback sent.", "Feedback ")
    return "done"

def send_stop_processing_notification(decision, decision_user):
    template = constants.stop_processing_notification_email_template_html
    content = (
            template["body"]
            % (
                decision.request_id,
                decision_user.full_name,
                decision.request_id,
                decision.request_id,
            )
            + template["footer"]
            + "<br><br>"
            + str(constants.user_training_string)
        )

    msg = MIMEText(content, "html")
    msg['Subject'] = template["subject"] % (decision.request_id, decision.report)
    msg['From'] = NOTIFICATION_SENDER

    # the email header's "to" field is for display only, the actual to address is in the sendmail() params
    msg['To'] = IGO_BILLER

    s = smtplib.SMTP('localhost')
    s.sendmail(NOTIFICATION_SENDER, IGO_BILLER.split(","), msg.as_string())
    s.close()
    return "Sent notification to biller for manual charge addition." 