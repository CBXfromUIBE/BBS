from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from .models import LikeRecord,LikeCount,disLikeCount,disLikeRecord
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist

def ErrorResponse(code,message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def SuccessResponse(num):
    data={}
    data['status'] = 'SUCCESS'
    data['num'] = num
    return JsonResponse(data)

def like_change(request):
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

    if request.GET.get('is_like') == 'true':
        like_record,created = LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id , user=user)
        if created:
            like_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            like_count.liked_num +=1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            return ErrorResponse(402,'重复点赞')

    else:
        if LikeRecord.objects.filter(content_type=content_type,object_id=object_id , user=user).exists():
            like_record = LikeRecord.objects.get(content_type=content_type,object_id=object_id , user=user)
            like_record.delete()
            like_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            if not created:
                like_count.liked_num -=1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(404,'数据错误')
        else:
            return ErrorResponse(403,'没有点赞')

def dislike_change(request):
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

    if request.GET.get('is_dislike') == 'true':
        dislike_record,created = disLikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id , user=user)
        if created:
            dislike_count,created = disLikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            dislike_count.disliked_num +=1
            dislike_count.save()
            return SuccessResponse(dislike_count.disliked_num)
        else:
            return ErrorResponse(402,'重复点淦')

    else:
        if disLikeRecord.objects.filter(content_type=content_type,object_id=object_id , user=user).exists():
            dislike_record = disLikeRecord.objects.get(content_type=content_type,object_id=object_id , user=user)
            dislike_record.delete()
            dislike_count,created = disLikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            if not created:
                dislike_count.disliked_num -=1
                dislike_count.save()
                return SuccessResponse(dislike_count.disliked_num)
            else:
                return ErrorResponse(404,'数据错误')
        else:
            return ErrorResponse(403,'没有点赞')
# 