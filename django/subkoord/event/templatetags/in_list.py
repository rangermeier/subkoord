from django import template

register = template.Library()

@register.filter
def in_list(value,arg):
  """ {% if item|in_list:list %} """
  return value in arg


