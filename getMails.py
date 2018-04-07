from __future__ import print_function
import httplib2
import os

# for db session sqlite import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, MailTable, Label

#for unicode to string
import unicodedata

#for gmail python client
import base64
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import errors

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

#let's Connect to Database and create database session
engine = create_engine('sqlite:///mails.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and stores some message in database
    from the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    #let's get messages from google server
    try:
        response = service.users().messages().list(userId='me',
                                                   maxResults=500).execute()
        for x in response['messages']:
            mail_id = x['id']
            #let's get the message from server
            headers = ['X-Original-To','Message-ID','Date','Delivered-To']
            message = service.users().messages().get(userId='me', id=mail_id,
                                                     format='full').execute()
            date_of_mail_long_ms = message['internalDate']
            #let's get all the labeles of this mail
            mail_labels = message["labelIds"]
            #let's get headers for subject, to, and from
            headers = message['payload']['headers']
            # we need to convert unicode to string so we can save them into database
            for x in headers:
                if x['name'].decode('unicode_escape') == "Subject":
                    mail_subject = unicodedata.normalize('NFKD', x['value']).encode('ascii','ignore')
            for x in headers:
                if x['name'].decode('unicode_escape') == "From":
                    mail_from = unicodedata.normalize('NFKD', x['value']).encode('ascii','ignore')
            for x in headers:
                if x['name'].decode('unicode_escape') == "To":
                    mail_to = unicodedata.normalize('NFKD', x['value']).encode('ascii','ignore')
            # Gmail api's sends different response, depending on the mail format, so
            #  we have to deal with different responses
            if message['payload']['body'].get('data'):
                mail_text = base64.urlsafe_b64decode(
                    message['payload']['body']['data'].encode("UTF8"))
            elif message['payload']['parts'][0]['body'].get('data'):
                mail_text = base64.urlsafe_b64decode(message['payload']['parts'][0]['body']['data'].encode("UTF8"))
                print('counted')
            else:
                messages = message['payload']['parts'][0]['parts']
                for x in messages:
                    if x['mimeType'].decode('unicode_escape') =='text/plain':
                        mail_text = base64.urlsafe_b64decode(x['body']['data'].encode("UTF8"))
            newMailObj = MailTable( mail_id=mail_id,
                                    mail_time=date_of_mail_long_ms,
                                    mail_from=mail_from,
                                    mail_to=mail_to,
                                    subject=mail_subject,
                                    text_of_body=mail_text.decode('unicode_escape'))
            session.add(newMailObj)
            session.commit()
            #now lets add label for this mail
            for x in mail_labels:
                label=unicodedata.normalize('NFKD', x).encode('ascii','ignore');
                new_Label_obj = Label(mail_label = label, mail_id=mail_id )
                session.add(new_Label_obj)
                session.commit()
    except errors.HttpError, error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()