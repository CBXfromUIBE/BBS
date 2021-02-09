from django import template
from django.contrib.contenttypes.models import  ContentType
from ..models import Comment
from django.db.models.fields import exceptions

register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    try:
        content_type = ContentType.objects.get_for_model(obj) 
        comment_count = Comment.objects.filter(content_type=content_type,object_id=obj.pk).count()
        return comment_count
    except exceptions.ObjectDoesNotExist:
        return 0