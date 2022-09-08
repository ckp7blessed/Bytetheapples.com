from django import template
from django.template.defaultfilters import stringfilter
from blog.models import Notification
import requests

register = template.Library()


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

#value.split(delimiter) example
#March 28, 2022 ['1', 'day,'] ago
#March 29, 2022 ['23', 'hours,'] ago
#March 30, 2022 ['11', 'minutes'] ago

@register.filter
def gtoe(a, b):
    return a >= b

@register.inclusion_tag('blog/show_notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    notifications = Notification.objects.filter(to_user=request_user).exclude(user_has_seen=True).order_by('-date')
    return {'notifications':notifications}

@register.inclusion_tag('blog/news_feed.html', takes_context=True)
def news_feed(context):
    r = requests.get(
        'http://api.mediastack.com/v1/news?access_key=ACCESS_KEY&countries=us&languages=en&limit=3&categories=technology')
    res = r.json()
    data = res['data']
    title = []
    description = []
    image = []
    url = []
    source = []
    for i in data:
        title.append(i['title'])
        description.append(i['description'])
        image.append(i['image'])
        url.append(i['url'])
        source.append(i['source'])
    news = zip(title, description, image, url, source)
    return {'news': news}