# for db session sqlite import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, MailTable, Label, Archive
import datetime
import time

Field = ["From", "To", "Subject", "Date Received"]
predicates_for_string = ["contains", "Does not contain", "equals", "not equals"]
predicates_for_date = ["greater than", "less than"]
actions = ["Mark as read", "mark as unread", "Archive message", "Add label"]

# let's Connect to Database and create database session
engine = create_engine('sqlite:///mails.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def main():
    predicate_list = []
    while True:
        new_rule = {}
        # selecting first parameter from ["From", "To",  "Subject", "Date Received" ]
        print("type q for quit, a for action")
        print("Select one field to apply predicate:-")
        for i, value in enumerate(Field):
            print("For " + value.upper() + " Enter " + str(i))
        print('enter q for quit.')
        input_value = raw_input("Your input:")
        if input_value == 'q':
            print("thanks for using this program.")
            break
        new_rule['field'] = Field[int(input_value)]

        # choosing predicate rule based on the selection either predicates_for_string or
        # from predicates_for_date
        print("choose predicate function")
        if int(input_value) == 3:
            new_rule['predicates_for_date'] = predicates_for_date[enumerate_list(predicates_for_date)]
        else:
            new_rule['predicates_for_string'] = predicates_for_string[enumerate_list(predicates_for_string)]
        # depending upon selection we are goiong to choose either search_string or time period (in days or months)
        if new_rule.get('predicates_for_string'):
            search_string = str(raw_input("Enter search string: "))
            new_rule['search_string'] = search_string
        else:
            options = ["days", "months"]
            print("what do you want to choose:")
            choosed_option = enumerate_list(options)
            new_rule['time_option'] = options[choosed_option]
            if choosed_option == 0:
                search_days = int(raw_input("insert search days: "))
                new_rule['search_days'] = search_days
            else:
                search_months = int(raw_input("insert search months: "))
                new_rule['search_days'] = search_months * 30
        predicate_list.append(new_rule)

        # We have selected our rules till now, lets see if we want to
        # add another rule or just want to see what we have choosen
        input_value = raw_input("To get answer for given predicate rules type (a),"
                                " if you want to add another rule type any other key. ")
        if input_value == 'a':
            condition = int(raw_input("What condition do you want to apply:\n"
                                      " for All type 0:\n "
                                      "for Any type 1:\n"
                                      "Your Input: "))
            if condition == 0:
                all = True
            else:
                all = False
            print("our rules are")
            for rule in predicate_list:
                if rule['field'] == "Date Received":
                    print(rule['field'] + " " + rule["predicates_for_date"] + " " + str(rule["search_days"]) + " days")
                else:
                    print(rule['field'] + " " + rule["predicates_for_string"] + " " + rule["search_string"])
            # now lets filter mails according to these rules
            filter_mail(predicate_list, all)
            break
        print("let's add more rule")


def enumerate_list(list_data):
    for i, value in enumerate(list_data):
        print("For " + value.upper() + " Enter " + str(i))
    return int(raw_input("Your input:"))


def filter_mail(predicate_list, all):
    mails = []
    if all:
        # all conditions should be true to get mail into mails
        mail_objects = session.query(MailTable)
        for mail in mail_objects:
            s = mail.mail_time
            should_break = False
            for predicate in predicate_list:
                if should_break:
                    break
                print(predicate)
                if predicate.get("predicates_for_date"):
                    current_time_in_ms = int(round(time.time() * 1000))
                    total_time_duration_for_query = 86400000 * predicate['search_days']
                    time_for_comparison = current_time_in_ms - int(total_time_duration_for_query)
                    if predicate["predicates_for_date"] == "greater than":
                        if s < time_for_comparison:
                            pass
                        else:
                            should_break = True
                    else:
                        # it is about less than
                        if s > time_for_comparison:
                            pass
                        else:
                            should_break = True
                else:
                    # it means that it is about some string, that contains or something equal
                    # Field = ["From", "To",  "Subject", "Date Received" ]
                    if predicate['field'] == 'From':
                        # predicates_for_string = ["contains", "Does not contain","equals", "not equals" ]
                        if predicate["predicates_for_string"] == "contains":
                            if mail.mail_from.find(predicate['search_string']) > -1:
                                pass
                            else:
                                should_break = True
                        if predicate["predicates_for_string"] == "Does not contain":
                            if mail.mail_from.find(predicate['search_string']) > -1:
                                should_break = True
                            else:
                                pass
                        if predicate["predicates_for_string"] == "equals":
                            if mail.mail_from == predicate['search_string']:
                                pass
                            else:
                                should_break = True
                        if predicate["predicates_for_string"] == "not equals":
                            if mail.mail_from == predicate['search_string']:
                                should_break = True
                            else:
                                pass
                    if predicate['field'] == 'To':
                        if predicate["predicates_for_string"] == "contains":
                            if mail.mail_to.find(predicate['search_string']) > -1:
                                pass
                            else:
                                should_break = True
                        if predicate["predicates_for_string"] == "Does not contain":
                            if mail.mail_to.find(predicate['search_string']) > -1:
                                should_break = True
                            else:
                                pass
                        if predicate["predicates_for_string"] == "equals":
                            if mail.mail_to == predicate['search_string']:
                                pass
                            else:
                                should_break = True
                        if predicate["predicates_for_string"] == "not equals":
                            if mail.mail_to == predicate['search_string']:
                                should_break = True
                            else:
                                pass
                    if predicate['field'] == 'Subject':
                        if predicate["predicates_for_string"] == "contains":
                            if mail.subject.find(predicate['search_string']) > -1:
                                pass
                            else:
                                should_break = True
                        if predicate["predicates_for_string"] == "Does not contain":
                            if mail.subject.find(predicate['search_string']) > -1:
                                should_break = True
                            else:
                                pass
                        if predicate["predicates_for_string"] == "equals":
                            if mail.subject == predicate['search_string']:
                                pass
                            else:
                                should_break = True
                        if predicate["predicates_for_string"] == "not equals":
                            if mail.subject == predicate['search_string']:
                                should_break = True
                            else:
                                pass
            if not should_break:
                mails.append(mail)
    else:
        # for any conditions, atleast one predicate must be true to add into mails
        mail_objects = session.query(MailTable)
        for mail in mail_objects:
            s = mail.mail_time
            for predicate in predicate_list:
                if predicate.get("predicates_for_date"):
                    current_time_in_ms = int(round(time.time() * 1000))
                    total_time_duration_for_query = 86400000 * predicate['search_days']
                    time_for_comparison = current_time_in_ms - int(total_time_duration_for_query)
                    if predicate["predicates_for_date"] == "greater than":
                        if s < time_for_comparison:
                            mails.append(mail)
                            break
                    else:
                        # it is about less than
                        if s > time_for_comparison:
                            mails.append(mail)
                            break
                else:
                    # it means that it is about some string, that contains or something equal
                    # Field = ["From", "To",  "Subject", "Date Received" ]
                    if predicate['field'] == 'From':
                        # predicates_for_string = ["contains", "Does not contain","equals", "not equals" ]
                        if predicate["predicates_for_string"] == "contains":
                            if mail.mail_from.find(predicate['search_string']) > -1:
                                mails.append(mail)
                                break
                        if predicate["predicates_for_string"] == "Does not contain":
                            if mail.mail_from.find(predicate['search_string']) > -1:
                                pass
                            else:
                                mails.append(mail)
                                break
                        if predicate["predicates_for_string"] == "equals":
                            if mail.mail_from == predicate['search_string']:
                                mails.append(mail)
                                break
                            else:
                                pass
                        if predicate["predicates_for_string"] == "not equals":
                            if mail.mail_from == predicate['search_string']:
                                pass
                            else:
                                mails.append(mail)
                                break
                    if predicate['field'] == 'To':
                        if predicate["predicates_for_string"] == "contains":
                            if mail.mail_to.find(predicate['search_string']) > -1:
                                mails.append(mail)
                                break
                            else:
                                pass
                        if predicate["predicates_for_string"] == "Does not contain":
                            if mail.mail_to.find(predicate['search_string']) > -1:
                                pass
                            else:
                                mails.append(mail)
                                break
                        if predicate["predicates_for_string"] == "equals":
                            if mail.mail_to == predicate['search_string']:
                                mails.append(mail)
                                break
                            else:
                                pass
                        if predicate["predicates_for_string"] == "not equals":
                            if mail.mail_to == predicate['search_string']:
                                pass
                            else:
                                mails.append(mail)
                                break
                    if predicate['field'] == 'Subject':
                        if predicate["predicates_for_string"] == "contains":
                            if mail.subject.find(predicate['search_string']) > -1:
                                mails.append(mail)
                                break
                            else:
                                pass
                        if predicate["predicates_for_string"] == "Does not contain":
                            if mail.subject.find(predicate['search_string']) > -1:
                                pass
                            else:
                                mails.append(mail)
                                break
                        if predicate["predicates_for_string"] == "equals":
                            if mail.subject == predicate['search_string']:
                                mails.append(mail)
                                break
                            else:
                                pass
                        if predicate["predicates_for_string"] == "not equals":
                            if mail.subject == predicate['search_string']:
                                pass
                            else:
                                mails.append(mail)
                                break
    # let's apply some action
    apply_action(mails)


def apply_action(mails):
    # we are going to do actions  according to this list
    # actions = ["Mark as read", "mark as unread", "Archive message", "Add label"]
    print("Enter your action: ")
    for i, value in enumerate(actions):
        print("For " + value.upper() + " Enter " + str(i))
    action_choice = int(raw_input("Enter your choice number: "))
    if action_choice == 0:
        # mark as read
        for x in mails:
            label_objects = session.query(Label).filter_by(mail_id=x.mail_id)
            for label in label_objects:
                if label.mail_label == "UNREAD":
                    session.delete(label)
                    session.commit()

    elif action_choice == 1:
        # mark as unread
        for x in mails:
            label_objects = session.query(Label).filter_by(mail_id=x.mail_id)
            applied = False
            for label in label_objects:
                if label.mail_label == "UNREAD":
                    applied = True
            if not applied:
                # if contrast label is not available, let's add this to file
                new_label_object = Label(mail_label="UNREAD", mail_id=x.mail_id)
                session.add(new_label_object)
                session.commit()
    elif action_choice == 2:
        # archieved message
        for x in mails:
            newArcheiveObj = Archive(mail_id=x.mail_id,
                                     mail_time=x.mail_time,
                                     mail_from=x.mail_from,
                                     mail_to=x.mail_to,
                                     subject=x.subject,
                                     text_of_body=x.text_of_body)
            session.add(newArcheiveObj)
            session.commit()
            # let's delete from mail file
            session.delete(x)
            session.commit()
    elif action_choice == 3:
        # add label
        label = raw_input("Enter your label name: ")
        for x in mails:
            newObj = Label(mail_label=label, mail_id=x.mail_id)
            session.add(newObj)
            session.commit()
    print("Congratulation, It has been applied. Aregorn")


if __name__ == '__main__':
    main()
