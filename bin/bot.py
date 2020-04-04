import html2text
import imap_connector
import imaplib
import re
import json
import time
import base64
import os

from getpass import getpass
from variables import *
from send_mail import send_email
from generate_body import *
from strip_tags import *
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# Password to start the bot

test = 3;
while test > 0:

    # get password for decryption
    password_provided = getpass() 
    passwordBytes = password_provided.encode()
    
    # i don't understand it but it works
    salt = b"emailslavebot" 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(passwordBytes))
    f = Fernet(key)
    
    # test if password is correct
    try:
        password = f.decrypt(encryptedpw).decode()
        
        break;
    except:
        test = test - 1
        print("Wrong password. " + str(test) + " tries left")

if test == 0:
    quit()

# helper to get number out of a string
numberRegex = "\d+"
def getNumber(string):
    n = re.search(numberRegex, string)
    if n:
        return n.group()
    return 0

cycles = 0

imapper = imap_connector.connect('imap.gmail.com', login, password)

while True:
    cycles += 1
    print("searching for command cycle {}...".format(cycles))  
    
    for mail_id in imapper.listids(20, '(UNSEEN)'):
        mail = imapper.mail(mail_id)
        if mail.title is None:
            title = ""
        else:
            title = mail.title
            
        commandsFromMessage = []
        responseBody = ""
        responseSubject = ""
        if (not mail.body.isspace()):
            mailBodyAsText = strip_tags(mail.body)
            commandsFromMessage = mailBodyAsText.split("\n")
            
        if re.findall("about", (title + mail.body).lower()):
            responseSubject = responseSubjectAbout
            responseBody = aboutpage

        elif re.findall("help", (title + mail.body).lower()): 
            responseSubject = responseSubjectInstructions
            responseBody = generate_help()        
            
            
        elif re.findall("^i (need|want).*command", title.lower()):
            responseSubject = responseSubjectCommands
            amountCommands = getNumber(title)
            if int(amountCommands) != 0:
                pickedCommands = generate_commands(commandsFromMessage, amountCommands)
                if pickedCommands != "":
                    responseBody = responseSafety + "<br>" + pickedCommands
                    if re.findall("need", title.lower()):
                        responseBody = responseYouMust + responseBody
                
        if not responseBody == "":   
            send_email(str(mail.from_addr), responseSubject, responseBody, password)
        else:
            send_email(str(mail.from_addr), """Something wrent wrong""", errormessage, password)

        print(str(mail_id) + " processed!")
        
    # reconnecting to the imap server, since connections get automatically closed after a while    
    if cycles % 2 == 0:
        imapper.quit()
        imapper = imap_connector.connect('imap.gmail.com', login, password)
        
    print("sleeping...")
    time.sleep(30)

