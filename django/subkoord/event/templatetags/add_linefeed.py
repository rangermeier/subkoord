from django import template
from django.utils.safestring import mark_safe
import re

def add_linefeed_filter(value, num=1):
	f = '  '*num
	p = re.compile("\n")
	value = p.sub(r'\n'+f, value)
	return mark_safe(value)

register = template.Library()
register.filter('add_linefeed', add_linefeed_filter)
