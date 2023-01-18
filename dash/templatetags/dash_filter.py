from django import template
import markdown
from django.utils.safestring import mark_safe
import json


register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))

@register.filter
def json_loads(value):
    return json.loads(value)

@register.filter
def get_dict(dictionary, key):
    return dictionary.get(key)

@register.filter
def to_krw(num):
    num = int(num)
    return format(num, ',')

@register.filter
def add_one(num):
    return num + 1

@register.filter
def rounded(num):
    return round(num, 2)