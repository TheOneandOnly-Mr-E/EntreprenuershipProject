import email
import os
import smtplib
import imaplib
import time
running = True

senderemail = "coronavirusmessagingteam@gmail.com"
pas = "zhtgbxwqnlkqaosg"
smtp = "smtp.gmail.com"
port = 587
server = smtplib.SMTP(smtp,port)

# Defines the email and app-specific password to use}
EMAIL = "coronavirusmessagingteam@gmail.com"
PAS = "zhtgbxwqnlkqaosg"
# Defins the IMAP server to use
SERVER = "imap.gmail.com"

'''# Connects to the server and selects inbox
inbox = imaplib.IMAP4_SSL(SERVER)
inbox.login(EMAIL,PAS)
inbox.select('inbox')'''

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

def replySend():
    try:
        command, recipient = messageCheck()
        '''email = "coronavirusmessagingteam@gmail.com"
        pas = "zhtgbxwqnlkqaosg"
        smtp = "smtp.gmail.com"
        port = 587
        server = smtplib.SMTP(smtp,port)'''
        server.starttls()
        #server.login(senderemail,pas)
        server.connect(smtp, port)
        if command == '!help':
            message = "!help - Displays a list of commands\n!unsubscribe - Unsubscribes you from the CMT\n!recent - Displays the most recent CMT message"
        elif command == '!subscribe':
            recipient_list = os.open("recipientlist.txt" , "a")
            recipient_list.write(",'"+recipient+"'")
            recipient_list.close()
            message = "Congratulations! You have subscribed to the Coronavirus Messaging Team's updates! Please send the message (!help) without parentheses to see all available commands."
        else:
            message = 'Please input a proper command. If you need a list of commands, send the message "!help" without quotation marks.'
        cleanInbox()
        server.sendmail(senderemail,recipient,message)
        server.quit()
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
    time.sleep(1)
    replySend()
