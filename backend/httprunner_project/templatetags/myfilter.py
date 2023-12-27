import time

from django import template

register = template.Library()


# {{ '%0.3f'| format(test_suite_summary.time.duration|float) }}


@register.filter(name='duration')
def duration(value):
    try:
        r = '%.2f' % value
    except:
        r = ''
    return r


@register.filter(name='format_time')
def format_time(value):
    """
    自定义过滤器
    """
    try:
        s = time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime(value))
    except:
        s = ''
    return s
