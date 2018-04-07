
Field = ["From", "To",  "Subject", "Date Received" ]
predicates_for_string = ["contains", "Does not contain","equals", "not equals" ]
predicates_for_date = ["greater than", "less than"]

actions = ["mark as read","mark as unread","archieve message", "Add label"]


def main():
    predicate_list=[]
    while True:
        new_rule={}
        # selecting first parameter from ["From", "To",  "Subject", "Date Received" ]
        print("type q for quit, a for action")
        print("Select one field to apply predicate:-")
        for i,value in enumerate(Field):
            print("For " + value.upper() +" Enter "+ str(i))
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
            new_rule['predicates_for_date']=predicates_for_date[enumerate_list(predicates_for_date)]
        else:
            new_rule['predicates_for_string'] =predicates_for_string[enumerate_list(predicates_for_string)]
        # depending upon selection we are goiong to choose either search_string or time period (in days or months)
        if new_rule.get('predicates_for_string'):
            search_string = str(raw_input("Enter search string: "))
            new_rule['search_string'] = search_string
        else:
            options = ["days","months"]
            print("what do you want to choose:")
            choosed_option = enumerate_list(options)
            new_rule['time_option'] = options[choosed_option]
            if choosed_option == 0:
                search_days=int(raw_input("insert search days: "))
                new_rule['search_days'] = search_days
            else :
                search_months = int(raw_input("insert search months: "))
                new_rule['search_days'] = search_months*30
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
                    print(rule['field']+" " + rule["predicates_for_date"] + " " + str(rule["search_days"])+" days" )
                else:
                    print(rule['field'] + " " + rule["predicates_for_string"] + " " + rule["search_string"])
            #now action time
            apply_action(predicate_list,all)
            break
        print("let's add more rule")


def enumerate_list(list_data):
    for i, value in enumerate(list_data):
        print("For " + value.upper() + " Enter " + str(i))
    return int(raw_input("Your input:"))


def apply_action(predicate_list, all):
    mails=[]
    if all:
        pass
        #all conditions should be true
    else:
        pass
        #anyconditions

if __name__ == '__main__':
    main()