############################################################################################
# Sends an email notification in the event of an error
############################################################################################

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

MAILTO = 'destinyclantracker@gmail.com'
MAILFROM = 'destinyclantracker@gmail.com'
MAILMULTI = ['destinyclantracker@gmail.com','adamseamil@adamseamil.com']
PASSWORD = 'roxie301'
COMMASPACE = ','
#SERVER = smtplib.SMTP('smtp.gmail.com', 587)

def sendMessageOld(msg):
    ## --OUTDATED-- ##
    SERVER = smtplib.SMTP('smtp.gmail.com', 587)
    SERVER.ehlo()
    SERVER.starttls()
    SERVER.login(MAILTO, PASSWORD)

    SERVER.sendmail(MAILFROM, MAILTO, msg)
    SERVER.quit()
    
def sendMessage(msg, sbjt):

    # Message info
    outer = MIMEMultipart()
    outer['Subject'] = sbjt
    outer['To'] = MAILTO
    outer['From'] = MAILFROM
    outer.preamble = "I don't know what this is TBH"
    outer.attach(MIMEText(msg))

    # Convert to string
    composed = outer.as_string()

    # Send the message
    SERVER = smtplib.SMTP('smtp.gmail.com', 587)
    SERVER.ehlo()
    SERVER.starttls()
    SERVER.login(MAILTO, PASSWORD)

    SERVER.sendmail(MAILFROM, MAILTO, composed)
    SERVER.quit()