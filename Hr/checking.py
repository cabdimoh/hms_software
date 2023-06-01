# from datetime import date
# schedula = "Tuesday,Sunday,Tuesday"
# today = date.today()
# day_name = today.strftime("%A")


# def checkpresent():
#         checker = False
#         today = date.today()
#         day_name = today.strftime("%A")
#         days = schedula.split(',')
#         for d in days:
#             if d == day_name:    
#                 checker = True  
#             else:
#                 checker = False
                   
#         return checker

# print(checkpresent())


import datetime


def number_to_words(num):
    ones = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    tens = ['ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    teens = ['eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
    if num == 0:
        return 'zero'
    if num < 0:
        return 'minus ' + number_to_words(abs(num))
    words = ''
    if num // 1000 > 0:
        words += number_to_words(num // 1000) + ' thousand '
        num %= 1000
    if num // 100 > 0:
        words += ones[num // 100] + ' hundred '
        num %= 100
    if num >= 11 and num <= 19:
        words += teens[num - 11] + ' '
        return words
    elif num == 10 or num >= 20:
        words += tens[num // 10 - 1] + ' '
        num %= 10
    if num > 0:
        words += ones[num] + ' '
    return words.strip()
    
# Example usage:

words = number_to_words(65)
print(words)


current_date = datetime.datetime.today().date()
print(current_date)


todays = datetime.date.today()
day_names = todays.strftime("%A")     
print(day_names) 


day = 'Saturday, sunday,Monday'
day = day.split(',')

for d in day:
    if d == day_names:
        print('today is present')
    else:
        print('today is not working')


                    # shiftid = [x for x in shiftid.split(',')]

                    # for index, item in enumerate(employe):
                    #     setemploye = Attandence(
                    #             employee_id = item, shift_id = shiftid[index],today_date = currentDate, state = status[xrow])
