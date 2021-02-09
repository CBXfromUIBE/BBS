from django import template
from django.contrib.contenttypes.models import  ContentType
from ..models import Heart_Favor

register = template.Library()

@register.simple_tag(takes_context=True)
def get_heart_status(context,obj):
    try:
        content_type = ContentType.objects.get_for_model(obj)
        user = context['user']
        if not user.is_authenticated:
            return ''
        if Heart_Favor.objects.filter(content_type=content_type,object_id=obj.pk,user=user).exists():
            return 'active'
        else:
            return ''
    except:
        return ''

@register.simple_tag(takes_context=True)
def get_favor_status(context,obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if Heart_Favor.objects.filter(content_type=content_type,object_id=obj.pk,user=user).exists():
        return 'active'
    else:
        return ''