# project to Implement a python gamil client command line application

## This project implements following predicate rules and actions on mail
Implement the following set:
Fields: From, To, Subject, Message, Received Date/Time Predicate:
- For string type fields - Contains, Does not Contain, Equals, Does not equal
- For date type field (Received) - Less than / Greater than for days / months. Actions:
- Mark as read / mark as unread
- Archive message
- Add label

## steps for configuration
1. first go to google gmail console and 
register for gmail API, a google search
 might help, search google gmail python client.
2.save the credential as client_secret.json

## steps to run the project
1. Install dependencies for this project run command:<br>
pip install -r requirements.txt
2. now create the database by command:<br>
 python model.py
3. now let's get mails from your gmail account by running command:<br>
python getMails.py
4. now let's apply predicate rules and actions on saved mails in database:<br>
python predicate.py

### The program will automatically guide you, how to apply predicates and actions 