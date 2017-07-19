import datetime

def check_phone_number(number):
    if(number.startswith("+88")):
        number = number[3:]
    elif (number.startswith("88")):
        number = number[2:]
    if(len(number)!=11):
        return False
    if(number.isnumeric()==False):
        return False
    if(number.startswith("015") or number.startswith("016") or number.startswith("018")
       or number.startswith("017") or number.startswith("019")):
        return True
    return False
def check_date(dateformat):

    try:
        newDate = datetime.datetime(int(dateformat[0]), int(dateformat[1]), int(dateformat[2]))
        #print(dateformat[0],dateformat[1],dateformat[2])
    except ValueError as err:
        #print(err)
        return False
    return True