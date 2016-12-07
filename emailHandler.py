############################################################################################
# Sends an email notification in the event of an error
############################################################################################

import smtplib
from email.mime.text import MIMEText

MAILTO = 'destinyclantracker@gmail.com'
MAILFROM = 'destinyclantracker@gmail.com'
PASSWORD = 'roxie301'
# SERVER = smtplib.SMTP('smtp.gmail.com', 587)

def sendMessage(msg):
    SERVER = smtplib.SMTP('smtp.gmail.com', 587)
    SERVER.ehlo()
    SERVER.starttls()
    SERVER.login(MAILTO, PASSWORD)

    SERVER.sendmail(MAILFROM, MAILTO, msg)
    SERVER.quit()
    

