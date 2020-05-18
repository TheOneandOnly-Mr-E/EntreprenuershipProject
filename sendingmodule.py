import smtplib
import os

email = "coronavirusmessagingteam@gmail.com"
pas = "zhtgbxwqnlkqaosg"

recipient_list = '9259995526@vtext.com'
# Defines the smtp server and port to use to send messages
smtp = "smtp.gmail.com"
port = 587
server = smtplib.SMTP(smtp,port)
# Starts the server
server.starttls()
# Logs into the server
server.login(email,pas)

sms = "(Coronavirus Messaging Team Update)\nThis is a test message."

server.sendmail(email,recipient_list,sms)

# lastly quit the server
server.quit()
