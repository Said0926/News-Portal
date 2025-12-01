from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='has_group')
def has_group(user, group_name):
    """Проверяет, принадлежит ли пользователь к указанной группе"""
    return user.groups.filter(name=group_name).exists()