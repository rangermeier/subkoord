from django import template
from django.utils.safestring import mark_safe
import re

def highlight_email_filter(value):
    p = re.compile("([\.\w-]+@[\w-]+\.[\w-]+)")
    value = p.sub(r'<strong>\1</strong>', value)
    return mark_safe(value)

register = template.Library()
register.filter('highlight_email', highlight_email_filter)
