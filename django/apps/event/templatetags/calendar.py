# Template tag
from datetime import date, timedelta

from django import template
from event.models import Event # You need to change this if you like to add your own events to the calendar

register = template.Library()


def get_last_day_of_month(year, month):
    if (month == 12):
        year += 1
        month = 1
    else:
        month += 1
    return date(year, month, 1) - timedelta(1)


def month_cal(year, month):

    first_day_of_month = date(year, month, 1)
    last_day_of_month = get_last_day_of_month(year, month)
    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())
    last_day_of_calendar = last_day_of_month + timedelta(7 - last_day_of_month.weekday())

    event_list = Event.objects.filter(date__gte = first_day_of_calendar,
        date__lte = last_day_of_calendar)

    month_cal = []
    week = []
    week_headers = []

    i = 0
    day = first_day_of_calendar
    while day <= last_day_of_calendar:
        if i < 7:
            week_headers.append(day)
        cal_day = {}
        cal_day['day'] = day
        cal_day['event'] = False
        cal_day['events'] = []
        for event in event_list:
            if day == event.date.date():
                cal_day['event'] = True
                cal_day['events'].append(event)
        if day.month == month:
            cal_day['in_month'] = True
        else:
            cal_day['in_month'] = False
        cal_day['today'] = day == date.today()
        cal_day['future'] = day >= date.today()
        week.append(cal_day)
        if day.weekday() == 6:
            month_cal.append(week)
            week = []
        i += 1
        day += timedelta(1)

    controls = {}
    previous = first_day_of_month - timedelta(days=1)
    controls['previous_year'] = previous.year
    controls['previous_month'] = previous.month
    next = last_day_of_month + timedelta(days=1)
    controls['next_year'] = next.year
    controls['next_month'] = next.month
    controls['this_month'] = first_day_of_month
    today = date.today()
    jumpto_year = today.year
    controls['jumpto'] = []
    for m in range(0,6):
        jumpto_month = today.month + m
        if jumpto_month > 12:
            jumpto_month -= 12
            jumpto_year = today.year + 1
        controls['jumpto'].append({
            'year': jumpto_year,
            'month': jumpto_month})
    return {'calendar': month_cal, 'headers': week_headers, 'controls': controls}

register.inclusion_tag('event/month_cal.html')(month_cal)

"""
Put this in your template (in my case agenda/month_cal.html):

<table class="cal_month_calendar">
<tr>
{% for day in headers %}
<th>{{ day|date:"D"|slice:":2" }}</th>
{% endfor %}
</tr>
{% for week in calendar %}
<tr>
{% for day in week %}
<td{% if not day.in_month %} class="cal_not_in_month"{% endif %}>{% if day.event %}<a href="/calendar/{{ day.day|date:"Y/m" }}/">{{ day.day|date:"j" }}</a>{% else %}{{ day.day|date:"j" }}{% endif %}</td>
{% endfor %}
</tr>
{% endfor %}
</table>

"""
