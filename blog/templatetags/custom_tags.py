from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


# @register.filter
# @stringfilter
# def upto(value, delimiter=None):
#     return value.split(delimiter)[0:2]
# upto.is_safe = True

# @register.filter
# @stringfilter
# def upto(value, delimiter=None):
#     if value.split(delimiter)[1] == "day" or "day," or "days":
#         if int(value.split(delimiter)[0]) < 6:
#             if int(value.split(delimiter)[0]) != 0:
#                 num_days = value.split(delimiter)[0:2]
#                 num_days[1] = 'd'
#                 return "".join(num_days)
#     if value.split(delimiter)[1] == "hour" or "hours" or "hours,":
#         if int(value.split(delimiter)[0]) < 23: 
#             if int(value.split(delimiter)[0]) != 0:
#                 num_hours = value.split(delimiter)[0:2]
#                 num_hours[1] = 'h'
#                 return "".join(num_hours)
#     if value.split(delimiter)[1] == "minute" or "minutes" or "minutes,":
#         if int(value.split(delimiter)[0]) < 59: 
#             if int(value.split(delimiter)[0]) != 0:
#                 num_minutes = value.split(delimiter)[0:2]
#                 num_minutes[1] = 'min'
#                 return "".join(num_minutes)
#             else: 
#                 return "Just Now"
#     else:
#         return "show_date"
# upto.is_safe = True


days = ["day", "day,", "days", "days,"]
hours = ["hour", "hour,", "hours", "hours," ]
minutes = ["minute", "minute,", "minutes", "minutes,"]

@register.filter
@stringfilter
def upto(value, delimiter=None):
    if value.split(delimiter)[1] in days:
        if int(value.split(delimiter)[0]) < 7:
            if int(value.split(delimiter)[0]) != 0:
                num_days = value.split(delimiter)[0:2]
                num_days[1] = 'd'
                return "".join(num_days)
    elif value.split(delimiter)[1] in hours:
        if int(value.split(delimiter)[0]) < 24: 
            if int(value.split(delimiter)[0]) != 0:
                num_hours = value.split(delimiter)[0:2]
                num_hours[1] = 'h'
                return "".join(num_hours)
    elif value.split(delimiter)[1] in minutes:
        if int(value.split(delimiter)[0]) < 60: 
            if int(value.split(delimiter)[0]) != 0:
                num_minutes = value.split(delimiter)[0:2]
                num_minutes[1] = 'min'
                return " ".join(num_minutes)
            else: 
                return "Just Now"
    else:
        return "show_date"
upto.is_safe = True

@register.filter
def gtoe(a, b):
    return a >= b


#original
#March 28, 2022 1 day, 23 hours ago
#March 29, 2022 23 hours, 35 minutes ago
#March 30, 2022 10 minutes ago


#current
#March 28, 2022 ['1', 'day,'] ago
#March 29, 2022 ['23', 'hours,'] ago
#March 30, 2022 ['11', 'minutes'] ago