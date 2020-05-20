import smtplib
import os

email = "coronavirusmessagingteam@gmail.com"
pas = "zhtgbxwqnlkqaosg"

def getRcpts():
    rclist = []
    rcstring = ""
    rcptexists = False
    recipientList = open("recipientlist.txt", "r")
    recipients = recipientList.read()
    for r in recipients:
        if r == " ":
            rclist.append(rcstring)
            rcstring = ""
        elif r != " ":
            rcstring += r
    return rclist

recipient_list = getRcpts()

# Defines the smtp server and port to use to send messages
smtp = "smtp.gmail.com"
port = 587
server = smtplib.SMTP(smtp,port)
# Starts the server
server.starttls()
# Logs into the server
server.login(email,pas)

sms = "(Coronavirus Messaging Team Update)\n\n" + input("Input the message to send here: ")

server.sendmail(email,recipient_list,sms)

# lastly quit the server
server.quit()
