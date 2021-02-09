import datetime
from django.shortcuts import render,get_object_or_404,redirect
from tiezi.models import TieZi,TieZi_Label
from read_statistics.models import ReadNum
from read_statistics.views import oneday
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.cache import cache
from django.urls import reverse
from django.db.models import Sum
from user.forms import LoginForm




def get_newest_tiezi():
    x = TieZi.objects.all()
    true_list = []
    for i in range(10):
        true_list.append(x[i])
    return true_list

#按时期归档，还未用到
def time_statistic():
    tiezi_dates = TieZi.objects.dates('created_time','month',order='DESC')
    for i in tiezi_dates:
        time_statistic = TieZi.objects.filter(created_time__year=i.year,  \
                            created_time__month=i.month).count()
    return time_statistic

def get_hotest_tiezi():
    x = ContentType.objects.get_for_model(TieZi)
    read_rank=ReadNum.objects.filter(content_type=x).order_by('-read_num')[0:10:1]
    return  read_rank
    
def sevendays_hot_tiezi():   
    today = timezone.now().date() 
    date = today - datetime.timedelta(days=7)
    tiezi = TieZi.objects\
            .filter(read_detail__date__lt=today, read_detail__date__gt=date)\
            .values('id','title')\
            .annotate(read_num=Sum('read_detail__read_num'))\
            .order_by('-read_num')
    return tiezi[:7]

def month_hot_tiezi():   
    today = timezone.now().date() 
    date = today - datetime.timedelta(days=30)
    tiezi = TieZi.objects\
            .filter(read_detail__date__lt=today, read_detail__date__gt=date)\
            .values('id','title')\
            .annotate(read_num=Sum('read_detail__read_num'))\
            .order_by('-read_num')
    return tiezi[:7]

def tour_index(request):
    hotest_tiezi = cache.get('hotest_tiezi')
    if hotest_tiezi is None:
        hotest_tiezi = get_hotest_tiezi()
        cache.set('hotest_tiezi', hotest_tiezi, 60*60)
        print('calc')
    else:
        print('use caches')
    newest_tiezi = cache.get('newest_tiezi')
    if newest_tiezi is None:
        z = get_newest_tiezi()
        cache.set('newest_tiezi', z, 60*60)
        print('calc')
    else:
        print('use caches')
    context = {}
    context['hotest_tiezi'] = get_hotest_tiezi()   
    #context['today_read_num'] = today_read_num 未用到
    context['newest_tiezi'] = get_newest_tiezi()
    context['tiezi_all']  = TieZi.objects.all()
    return render(request, 'tour_index.html', context)

def index(request):
    #today_read_num = oneday(x) #方法在read_statistics里
    if not request.user.is_authenticated:
        login_form = LoginForm()
        context = {}
        context['login_form'] = login_form
        return render(request, 'user/login.html', context)

    #首页数据缓存
    
    hotest_tiezi = cache.get('hotest_tiezi')
    if hotest_tiezi is None:
        hotest_tiezi = get_hotest_tiezi()
        cache.set('hotest_tiezi', hotest_tiezi, 60*60)
        print('calc')
    else:
        print('use caches')
    newest_tiezi = cache.get('newest_tiezi')
    if newest_tiezi is None:
        z = get_newest_tiezi()
        cache.set('newest_tiezi', z, 60*60)
        print('calc')
    else:
        print('use caches')
    context = {}
    context['hotest_tiezi'] = get_hotest_tiezi()   
    #context['today_read_num'] = today_read_num 未用到
    context['newest_tiezi'] = get_newest_tiezi()
    context['tiezi_all']  = TieZi.objects.all()
    return render(request, 'index.html', context)


