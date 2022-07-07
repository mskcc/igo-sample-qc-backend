from app import app, db, constants
from app.logger import log_email, log_error, log_lims
from notify import send_decision_reminder_notification
import threading
import time
import schedule


def sendDecisionReminderEmail():
    print('sending email(s)')

def findDecisionPendingProjects():
    print('lims query here')

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every().day.at("08:30").do(run_threaded, sendDecisionReminderEmail)

while True:
    schedule.run_pending()
    time.sleep(1)
