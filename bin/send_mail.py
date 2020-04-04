import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from variables import *
from strip_tags import *

def send_email(receiver, subject, body, password):
    if body.isspace():
        return

    sender = login

    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    
    msg.attach(MIMEText(strip_tags(body), "plain"))
    msg.attach(MIMEText(body, "html"))

    smtpObj = smtplib.SMTP("""smtp.gmail.com:587""")
    try:
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(login, password)
    except:
        print("""Login attempt failed""")
    smtpObj.sendmail(sender, receiver, msg.as_string())
#    print("SENT: " + msg.as_string())