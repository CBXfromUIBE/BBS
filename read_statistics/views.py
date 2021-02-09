import datetime
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum,ReadDetail

# Create your views here.
def sevendays_all (content_type):
    today = timezone.now().date()
    dates = list()
    read_list = list()
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        detail = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = detail.aggregate(read_total=Sum('read_num'))
        read_list.append(result['read_total'] or 0)
    return dates, read_list

def oneday(content_type):
    today = timezone.now().date()
    detail = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return detail

def yesterday(content_type):
    yesterday = timezone.now().date() - datetime.timedelta(days=1)
    detail = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return detail

#def sevendays(content_type):  在BBS的views里









