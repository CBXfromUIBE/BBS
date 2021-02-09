from django import template
from django.contrib.contenttypes.models import  ContentType
from ..models import ReadNum,ReadNumExpandMethod
from django.db.models.fields import exceptions

register = template.Library()

@register.simple_tag
def get_read_count(obj):
    try:
        x = ContentType.objects.get_for_model(obj)
        readnum = ReadNum.objects.get(content_type=x, object_id=obj.pk)
        return readnum.read_num
    except exceptions.ObjectDoesNotExist:
        return 0
