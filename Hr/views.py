from django.shortcuts import render, redirect
from Users.models import sendException
from django.contrib.auth.decorators import login_required
from Users.views import sendTrials
from .models import *
# from  APEN.models import Specialities

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
import re

# regex variable  for validating inputs

validate_email = '^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+\.[a-zA-z]{2,3}$'
validate_text_only = '[a-zA-Z]'
validate_text_Number_only = '[A-Za-z0-9//,]'
validate_number_only = '[0-9]'
phone_validation = "^[0-9]+[0-9]+[0-9]{2,3}$"

# remove special character
def RemoveSpecialCharacters(text):
    # A list of special characters
    if text == '':
        return ''
    else:

        special_characters = ["+", "-", "&&", "||", "!", "(", ")", "{", "}", "[", "]", "^", "/", "=", "==", "<", ">", "$", "#", "/", ";", ",", "_", "%",
                              "~", "*", "?", ":", "\"", "\\"]
        # using lambda function to find if the special characters are in the list
        # Converting list to string using the join method
        normal_string = "".join(
            filter(lambda char: char not in special_characters, text))
        return normal_string

# start  text, email, number and alphanumeric


def check(email):

    if (re.search(validate_email, email)):
        return True
    else:
        return False


def phone_valid(phonevalid):

    if (re.match(phone_validation, phonevalid)):
        return True
    else:
        return False


def text_validation(text):

    if (re.match(validate_text_only, text)):
        return True
    else:
        return False


def number_validation(text):

    if (re.match(validate_number_only, text)):
        return True
    else:
        return False


def text_validationNumber(textnumber):

    if (re.match(validate_text_only, textnumber)):
        return True
    else:
        return False

# end

###################################  pre requirements ######################


def GenerateSerialNumber():
    last_id = Employee.objects.filter(~Q(emp_number=None)).last()
    serial = 0
    if last_id is not None:
        serial = int(last_id.emp_number[3:])
    serial = serial + 1

    if serial < 10:
        serial = '000' + str(serial)
    elif serial < 100:
        serial = '00' + str(serial)
    elif serial < 1000:
        serial = '0' + str(serial)

    return f"EMP{serial}"

def get_modified_date(start):
    timedelta = start
    seconds = timedelta.days * 24 * 3600 + timedelta.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)


    if days > 0:
        return f"{days} {'day' if days == 1 else 'days'} "

    if hours > 0:
        return f"{hours} {'hour' if hours == 1 else 'hours'} "

    if minutes > 0:
        return f"{minutes} {'minute' if minutes == 1 else 'minutes'} "

    return f"{seconds} {'second' if seconds == 1 else 'seconds'} "



def checkpresent(single_day):
        checker = False
        today = date.today()
        day_name = today.strftime("%A")
        days = single_day.split(',')
        for d in days:
            if d == day_name:    
                checker = True  
                break
            else:
                checker = False
                   
        return checker




def difference_date(start, end):
    start = [int(x) for x in start.split('-')]
    end = [int(x) for x in end.split('-')]

    start = date(start[0], start[1], start[2])
    end = date(end[0], end[1], end[2])

    timedelta = end - start
    seconds = timedelta.days * 24 * 3600 + timedelta.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    return days
