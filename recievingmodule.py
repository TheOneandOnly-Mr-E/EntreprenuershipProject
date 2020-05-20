import email
import imaplib
import keyboard
import os
import smtplib
import sys
import time
import pygame
import pygame.locals

running = True
recipient_list = []
timesRan = 0

senderemail = "coronavirusmessagingteam@gmail.com"
pas = "zhtgbxwqnlkqaosg"
smtp = "smtp.gmail.com"
port = 587
server = smtplib.SMTP()

pygame.init()
BLACK = (0,0,0)
WIDTH = 1280
HEIGHT = 1024
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

windowSurface.fill(BLACK)

# Defines the email and app-specific password to use}
EMAIL = "coronavirusmessagingteam@gmail.com"
PAS = "zhtgbxwqnlkqaosg"
# Defines the IMAP server to use
SERVER = "imap.gmail.com"

def cleanInbox():
    inbox = imaplib.IMAP4_SSL(SERVER)
    inbox.login(EMAIL,PAS)
    inbox.select('inbox')
    status, data = inbox.search(None, 'SEEN')
    for id in data[0].split():
        inbox.store(id, '+FLAGS', '\\Deleted')
    inbox.expunge()
    inbox.close()
    inbox.logout()

def sendQuit(msg, rcpt):
    server.connect(smtp,port)
    server.starttls()
    server.login(senderemail, pas)
    server.sendmail(senderemail, rcpt, msg)
    cleanInbox()
    server.rset()
    server.quit()

def subscriberCheck(rcpt):
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
    for r in rclist:
        if r == rcpt:
            rcptexists = True
    for r in recipient_list:
        if r == rcpt:
            rcptexists = True
    recipientList.close()
    return rcptexists

def unsubRcpt(rcpt):
    index = -1
    rclist = []
    rcstring = ""
    recipientList = open("recipientlist.txt", "r")
    recipients = recipientList.read()
    for r in recipients:
        if r == " ":
            rclist.append(rcstring)
            rcstring = ""
        elif r != " ":
            rcstring += r
    recipientList.close()
    for r in rclist:
        index += 1
        if r == rcpt:
            rclist.pop(index)
            recipientList = open("recipientlist.txt", "w")
            for r in rclist:
                recipientList.write(r)
                recipientList.close()
    return rclist

def replySend():
    try:
        command, recipient = messageCheck()
        if command == '!help':
            message = "!help - Displays a list of commands\n!unsubscribe - Unsubscribes you from the CMT service"
            sendQuit(message, recipient)
        elif command == '!subscribe':
            rcptexists = subscriberCheck(recipient)
            if rcptexists == True:
                message = "It appears you are already subscribed to the Coronavirus Messaging Team's updates!"
            elif rcptexists == False:
                recipient_list.append(recipient)
                recipientList = open("recipientlist.txt", "a")
                for r in recipient_list:
                    rstring = r + " "
                    recipientList.write(rstring)
                recipientList.close()
                message = "Congratulations! You have subscribed to the Coronavirus Messaging Team's updates! Please send the message (!help) without parentheses to see all available commands."
            sendQuit(message, recipient)
        elif command == '!unsubscribe':
            rcptexists = subscriberCheck(recipient)
            if rcptexists == False:
                message = "It appears you aren't subscribed to the Coronavirus Messaging Team's updates."
            elif rcptexists == True:
                recipient_list = unsubRcpt(recipient)
                message = "You are officially unsubscribed from the Coronavirus Messaging Team's updates. If you have any feedback to give, please do so at this link: https://forms.gle/ua7VpQrwZzCjRCek9"


        else:
            message = 'Please input a proper command. If you need a list of commands, send the message (!help) without parentheses.'
            sendQuit(message, recipient)
    except TypeError:
        pass


def messageCheck():
    # Connects to the server and selects inbox
    inbox = imaplib.IMAP4_SSL(SERVER)
    inbox.login(EMAIL,PAS)
    inbox.select('inbox')
    status, data = inbox.search(None, 'ALL')
    #Makes a list to store the ids of the mail messages
    id_list = []
    for block in data:
        #Iterates through the id list and seperates the message parts
        id_list += block.split()
    for i in id_list:
        #Fetches the email based on the id and format
        status, data = inbox.fetch(i, '(RFC822)')
        for mail in data:
            #Converts the email from bytes into raw data
            if isinstance(mail, tuple):
                #Grab important details from the raw data
                content = email.message_from_bytes(mail[1])
                sender = content['from']
                message_content = ''
                full_message = content.get_payload()
                for p in full_message:
                    if p.get_content_type() == 'text/plain':
                        message_content += p.get_payload()
                        return message_content, sender
    inbox.close()
    inbox.logout()

while running == True:
    print(timesRan)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                print("Program shutting down")
                recipientList = open("recipientlist.txt", "a")
                for r in recipient_list:
                    rstring = r + " "
                    recipientList.write(rstring)
                recipientList.close()
                pygame.quit()
                sys.exit()


    time.sleep(1)
    replySend()
    timesRan += 1
