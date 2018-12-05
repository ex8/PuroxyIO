from django import template

register = template.Library()


@register.filter
def format_data_size(num, suffix='B'):
    num = int(num)
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return '%3.1f %s%s' % (num, unit, suffix)
        num /= 1024.0
    return '%3.1f %s%s' % (num, 'Y', suffix)
