from django.shortcuts import render, get_object_or_404
from .models import TieZi,TieZi_Label
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum,ReadDetail
from django.utils import timezone
from django.db.models import Sum
from comment.models import Comment
from comment.forms import CommentForm
from user.forms import LoginForm

def tiezi_pagination(request, tiezi_list):
    paginator = Paginator(tiezi_list, settings.EACH_PAGE_TIEZI_NUM) #全类37篇帖子，分成8页
    which_page = request.GET.get('page',1)
    true_page = paginator.get_page(which_page)
    current_page_num = true_page.number
    page_range = list(range(max(current_page_num-1,1),current_page_num)) + \
    list(range(current_page_num,min(current_page_num+1,paginator.num_pages)+1))
    if page_range[0]-1>=1:
        page_range.insert(0,'···')
    if paginator.num_pages - page_range[-1] >=1:
        page_range.append('···')
    if page_range[0] !=1:
        page_range.insert(0,1)
    if page_range[-1] !=paginator.num_pages:
        page_range.append(paginator.num_pages)

    context={}
    context['tiezi_all']  = true_page.object_list #某一页的帖子集合
    context['page'] = true_page #分页器
    context['page_range'] = page_range

    return context
# Create your views here.
def tiezi_list(request):
    x = TieZi.objects.all()
    context = tiezi_pagination(request, x)  
    context['tiezi_all_count'] = TieZi.objects.all().count()
    context['tiezi_label_all'] = TieZi_Label.objects.all()
    context['tiezi_dates'] = TieZi.objects.dates('created_time', 'month', order="DESC")
    return render(request, 'tiezi_list.html', context);

def tiezi_detail(request, tiezi_id):
    x = ContentType.objects.get_for_model(TieZi)
    y = get_object_or_404(TieZi, pk=tiezi_id)

    if not request.COOKIES.get('tiezi_%s_read' % tiezi_id):
        
        readnum,created = ReadNum.objects.get_or_create(content_type=x,object_id=tiezi_id)
        readnum.read_num +=1
        readnum.save()
        date = timezone.now().date()
        readdetail,created = ReadDetail.objects.get_or_create(content_type=x,object_id=tiezi_id,date=date)     
        readdetail.read_num +=1
        readdetail.save()

    tiezi_content_type = ContentType.objects.get_for_model(TieZi)
    comment_all = Comment.objects.filter(content_type=tiezi_content_type,object_id=tiezi_id,parent=None) 
    context={}
    #context['user'] = request.user
    context['comment_count'] =Comment.objects.filter(content_type=tiezi_content_type,object_id=tiezi_id).count()
    context['comment_all'] = comment_all
    context['tiezi'] = y
    context['comment_form'] = CommentForm(initial={'content_type': tiezi_content_type.model, 'object_id': tiezi_id,'reply_comment_id':0})
    context['login_form'] = LoginForm()
    response = render(request,'tiezi_detail.html', context)
    response.set_cookie('tiezi_%s_read' % tiezi_id, 'true')
    return response

def label_to_tiezi(request, label_id):
    a = get_object_or_404(TieZi_Label, pk=label_id)
    x = TieZi.objects.filter(tiezi_label=a)
    context = tiezi_pagination(request, x)
    context['tiezi_all_count'] = TieZi.objects.all().count() #全类帖子总数
    context['tiezi_label_all'] = TieZi_Label.objects.all() #分类总集合 
    context['tiezi_label'] = a #该类名称
    context['tiezi_with_samelabel'] = x #该类帖子总集合
    return render(request, 'tiezi_with_samelabel.html', context)



