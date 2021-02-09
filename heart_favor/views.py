from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from .models import Heart_Favor
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist

def ErrorResponse(code,message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def SuccessResponse():
    data={}
    data['status'] = 'SUCCESS'
    return JsonResponse(data)

def heart_change(request):
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400,'没有登录')

    content_type = request.GET.get('content_type')
    object_id = request.GET.get('object_id')
    
    try:
        content_type = ContentType.objects.get(model=content_type) 
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401,'对象不存在')

    if request.GET.get('is_heart') == 'true':
        new_heart,created = Heart_Favor.objects.get_or_create(content_type=content_type,object_id=object_id , user=user)
        if created:
            return SuccessResponse()
        else:
            return ErrorResponse(402,'重复关注')

    else:
        if Heart_Favor.objects.filter(content_type=content_type,object_id=object_id , user=user).exists():
            heart_record = Heart_Favor.objects.get(content_type=content_type,object_id=object_id , user=user)
            heart_record.delete()
            return SuccessResponse()
        else:
            return ErrorResponse(403,'没有关注')

def favor_change(request):
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400,'没有登录')

    content_type = request.GET.get('content_type')
    object_id = request.GET.get('object_id')
    
    try:
        content_type = ContentType.objects.get(model=content_type) 
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401,'对象不存在')

    if request.GET.get('is_favor') == 'true':
        if Heart_Favor.objects.filter(content_type=content_type,object_id=object_id , user=user).exists():
            return ErrorResponse(402,'重复收藏')
        else:
            new_favor = Heart_Favor(content_type=content_type,object_id=object_id , user=user)
            new_favor.save()
            return SuccessResponse()         
    else:
        if Heart_Favor.objects.filter(content_type=content_type,object_id=object_id , user=user).exists():
            favor_record = Heart_Favor.objects.get(content_type=content_type,object_id=object_id , user=user)
            favor_record.delete()
            return SuccessResponse()
        else:
            return ErrorResponse(403,'没有收藏')


# 