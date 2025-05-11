from django import template

register = template.Library()

@register.filter
def times(number):
    if number:
        return range(int(number))

    return None

