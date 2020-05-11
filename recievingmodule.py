import email
import imaplib

# Defines the email and app-specific password to use}
email = "coronavirusmessagingteam@gmail.com"
pas = "zhtgbxwqnlkqaosg"
# Defins the IMAP server to use
server = "imap.gmail.com"

# Connects to the server and selects inbox
inbox = imaplib.IMAP4_SSL(server)
inbox.login(email,pas)
inbox.select(inbox)
