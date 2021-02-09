import string
import random
from time import *
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate, login , logout
from django.urls import reverse
from .forms import LoginForm,RegForm,ChangeUserInfoForm,ChangePasswordForm,ForgotPasswordForm
from tiezi.forms import TieZiForm
from tiezi.models import TieZi,TieZi_Label
from heart_favor.models import Heart_Favor
from comment.models import Comment
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import custom_user
from django.core.mail import send_mail
from django.db.models import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType

def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            return redirect(request.GET.get('from', reverse('index')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    context['tourist'] = 0
    return render(request, 'user/login.html', context)

def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def user_register(request):
    if request.method == 'POST':
        context = {} 
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            is_UIBEr = True
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = request.POST.get('email')
            if email.strip() == '':
                new_reg_form = RegForm()
                context = {}
                context['error_message'] = '邮箱不能为空'
                context['reg_form'] = new_reg_form
                return render(request, 'user/register.html', context)
            if User.objects.filter(email=email).exists():
                new_reg_form = RegForm()
                context = {}
                context['error_message'] = '邮箱已存在'  
                context['reg_form'] = new_reg_form
                return render(request, 'user/register.html', context)
            ver_code = request.POST.get('ver_code')
            code = request.session.get('ver_code', '')
            #验证是否为官邮
            if email.endswith('@uibe.edu.cn'):
                is_UIBEr = True
                #验证码是否为空
                if ver_code == '':
                    new_reg_form = RegForm()
                    context = {}
                    context['error_message'] = '验证码不能为空'
                    context['reg_form'] = new_reg_form
                    return render(request, 'user/register.html', context)
                #验证码是否正确
                if not (code != '' and code == ver_code):
                    new_reg_form = RegForm()
                    context = {}
                    context['error_message'] = '验证码不正确'
                    context['reg_form'] = new_reg_form
                    return render(request, 'user/register.html', context)
            else:
                is_UIBEr = False
            
            # 创建用户
            user = User.objects.create_user(username, email, password)
            new_one = custom_user.objects.create(user=user,is_UIBEr=is_UIBEr,nickname='') 
            user.save()
            new_one.save()
            if not code=='':
                del request.session['ver_code']
            # 登录用户
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('from', reverse('index')))
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)

def send_verification_code(request):    
    email = request.GET.get('email','')
    send_for_what = request.GET.get('send_for_what','')
    
    data = {}
    if send_for_what == 'send_for_register':
        if User.objects.filter(email=email).exists():
            data['status'] = 'ERROR'
            data['message'] = '该邮箱已被注册过' 
            return JsonResponse(data)
    if email != '': 
        subject ='UIBE.BBS【验证码】'
        from_email = '2180297171@qq.com'
        to_email = [email]
        code =''.join(random.sample(string.ascii_letters + string.digits, 6))
        message ='UIBE.BBS来信,以下是您的验证码:'+code+'，验证码5分钟内有效。'
        now = int(time())
        send_code_time = request.session.get('send_code_time',0)
        if now -send_code_time <30:
            data['status'] = 'ERROR'
            data['message'] = '婷婷'
        else:
            if send_for_what == 'send_for_register':
                request.session['ver_code'] = code
            if send_for_what == 'send_for_find_pwd':
                request.session['forgot_password_code'] = code
            request.session['send_code_time'] = send_code_time
            send_mail(
                subject,
                message,
                from_email,
                to_email,
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
        data['message'] = '错误'

    return JsonResponse(data)

def forget_pwd(request):
    return render(request, 'user/forget_pwd.html')

def user_logout(request):
    logout(request)
    return redirect(request.GET.get('from', reverse('index')))

def user_info(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']


    comment_list = Comment.objects.filter(user=request.user, parent=None)
    if comment_list.count() > 7:
        comment_list = comment_list[0:8]    
    join_tiezi = []
    for comment in comment_list:
        tiezi = TieZi.objects.get(id=comment.object_id)
        join_tiezi.append(tiezi)

    content_type = ContentType.objects.get(model='user')
    heart_user_list = Heart_Favor.objects.filter(user=request.user,content_type=content_type)
    if heart_user_list.count() > 4:
        heart_user_list = heart_user_list[0:5]

    content_type2 = ContentType.objects.get(model='tiezi')
    favor_tiezi_list = Heart_Favor.objects.filter(user=request.user,content_type=content_type2)
    if favor_tiezi_list.count() > 4:
        favor_tiezi_list = favor_tiezi_list[0:5]

    tiezi_list = TieZi.objects.filter(author=request.user)
    if tiezi_list.count() > 4:
        tiezi_list = tiezi_list[0:5]



    tiezi_form = TieZiForm()
    context={}
    context['ip'] = ip
    context['tiezi_form'] = tiezi_form
    context['join_tiezi'] = join_tiezi
    context['tiezi_list_top5'] = tiezi_list
    context['heart_user_list_top5'] = heart_user_list
    context['favor_tiezi_list_top5'] = favor_tiezi_list
    
    return render(request, 'user/new_user_info.html', context)
 
def update_tiezi(request):
    tiezi_form = TieZiForm(request.POST)
    data = {}

    if tiezi_form.is_valid():
        # 检查通过，保存数据
        tiezi = TieZi()
        tiezi.author = request.user
        tiezi.content = tiezi_form.cleaned_data.get('text','')
        tiezi.title = tiezi_form.cleaned_data.get('title','')
        tiezi_label_id = tiezi_form.cleaned_data.get('tiezi_label')
        label = TieZi_Label.objects.get(id=tiezi_label_id)
        tiezi.tiezi_label = label
        tiezi.save()

    return redirect(reverse('index'))

def change_userinfo(request):
    if request.method == 'POST':
        form = ChangeUserInfoForm(request.POST,user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            new_user,create = custom_user.objects.get_or_create(user=request.user)
            new_user.nickname = nickname_new
            new_user.save()
            return redirect(request.GET.get('from', reverse('index')))
    else:
        form = ChangeUserInfoForm()

    context = {}
    context['change_userinfo_form'] = form
    context['return_back_url'] = request.GET.get('from', reverse('index'))
    return render(request,'user/changeuserinfo.html',context)

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST,user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            old_password = form.cleaned_data['old_password']
            user=request.user
            user.set_password(new_password)
            user.save()
            logout(request)
            return redirect(reverse('index'))
    else:
        form = ChangePasswordForm()

    context = {}
    context['change_password_form'] = form
    context['return_back_url'] = request.GET.get('from', reverse('index'))
    return render(request,'user/change_password.html',context)

def forget_pwd(request):
    redirect_to = reverse('user_login')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        email = request.POST.get('email','')
        if not User.objects.filter(email=email).exists():
            new_form = ForgotPasswordForm()
            context = {}
            context['error_message'] = '邮箱不能为空'
            context['find_password_form'] = new_form
            return render(request, 'user/forget_pwd.html', context)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forgot_password_code']
            return redirect(redirect_to)    
    else:
        form = ForgotPasswordForm()

    context = {}
    context['find_password_form'] = form
    context['return_back_url'] = request.GET.get('from', reverse('index'))
    return render(request,'user/forget_pwd.html',context)

def manage_tiezi(request):
    context = {}
    user = request.user
    tiezi_of_user = TieZi.objects.filter(author=user)
    context['tiezi_of_user'] = tiezi_of_user
    context['return_back_url'] = reverse('user_info')
    return render(request,'user/my_tiezi.html',context)

def manage_comment(request):
    context = {}
    user = request.user
    comment_of_user = Comment.objects.filter(user=user)
    context['comment_of_user'] = comment_of_user
    context['return_back_url'] = reverse('user_info')
    return render(request,'user/my_comment.html',context)

def manage_heart_user(request):
    context = {}
    content_type = ContentType.objects.get(model='user')
    heart_user_list = Heart_Favor.objects.filter(user=request.user,content_type=content_type)
    context['heart_user_list'] = heart_user_list
    context['return_back_url'] = reverse('user_info')
    return render(request,'user/my_heart_user.html',context)

def manage_favor_tiezi(request):
    context = {}
    content_type = ContentType.objects.get(model='tiezi')
    favor_tiezi_list = Heart_Favor.objects.filter(user=request.user,content_type=content_type)
    context['favor_tiezi_list'] = favor_tiezi_list
    context['return_back_url'] = reverse('user_info')
    return render(request,'user/my_favor_tiezi.html',context)

def del_tiezi(request,tiezi_id):
    context = {}

    if not request.user is None: 
        try:
            TieZi.objects.get(id=tiezi_id).delete()
            return redirect( request.GET.get('from', reverse('index')) )
        except ObjectDoesNotExist:
            context['message'] = 'error'
            context['redirect_to'] = '/'
            return render(request,'error.html',context)

def del_comment(request,comment_id):
    context = {}

    if not request.user is None: 
        try:
            Comment.objects.get(id=comment_id).delete()
            return redirect( request.GET.get('from', reverse('index')) )
        except ObjectDoesNotExist:
            context['message'] = 'error'
            context['redirect_to'] = '/'
            return render(request,'error.html',context)

def get_ta_tiezi_all(request,ta_id):
    context = {}
    ta = User.objects.get(id=ta_id)
    ta_tiezi_all = TieZi.objects.filter(author=ta)
    context['ta_tiezi_list'] = ta_tiezi_all
    context['return_back_url']= reverse('manage_heart_user')
    return render(request,'user/ta_tiezi.html',context)

def cancel_heart(request,ta_id):
    try:
        content_type = ContentType.objects.get(model='user')
        heart_user =  Heart_Favor.objects.get(content_type=content_type,object_id=ta_id,user=request.user)
        heart_user.delete()
        return redirect( request.GET.get('from', reverse('index')) )
    except ObjectDoesNotExist:
        context['message'] = 'error'
        context['redirect_to'] = '/'
        return render(request,'error.html',context)

def cancel_favor(request,tiezi_id):
    try:
        content_type = ContentType.objects.get(model='tiezi')
        favor_tiezi =  Heart_Favor.objects.get(content_type=content_type,object_id=tiezi_id,user=request.user)
        favor_tiezi.delete()
        return redirect( request.GET.get('from', reverse('index')) )
    except ObjectDoesNotExist:
        context['message'] = 'error'
        context['redirect_to'] = '/'
        return render(request,'error.html',context)

    


