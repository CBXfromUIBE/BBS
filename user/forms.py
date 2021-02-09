from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='用户名或邮箱', 
                               widget=forms.TextInput(attrs={'class':'inputtext', 'placeholder':'请输入用户名或邮箱'}))
    password = forms.CharField(label='密码', 
                               widget=forms.PasswordInput(attrs={'class':'inputtext', 'placeholder':'请输入密码'})) 
    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='用户名', 
                               max_length=30,
                               min_length=2,
                               widget=forms.TextInput(attrs={'class':'inputtext', 'placeholder':'请输入2-30位用户名'}))
    password = forms.CharField(label='密码', 
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class':'inputtext', 'placeholder':'请输入密码,最少6位'}))
    password_again = forms.CharField(label='再输入一次密码', 
                                     min_length=6,
                                     widget=forms.PasswordInput(attrs={'class':'inputtext', 'placeholder':'再输入一次密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

class ChangeUserInfoForm(forms.Form):
    nickname_new = forms.CharField(label='新昵称', 
                                     max_length=20,
                                     widget=forms.TextInput(attrs={'class':'inputtext', 'placeholder':'输入新的昵称'}))

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new','').strip()
        if nickname_new =='':
            raise forms.ValidationError('你没有昵称吗？')
        return nickname_new

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeUserInfoForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='原密码', 
                                    min_length=6,
                                    widget=forms.PasswordInput(attrs={'class':'inputtext', 'placeholder':'输入原密码'}))
    new_password = forms.CharField(label='新密码',
                                    min_length=6,
                                    widget=forms.PasswordInput(attrs={'class':'inputtext', 'placeholder':'输入新密码'}))
    new_password_check = forms.CharField(label='密码确认', 
                                    min_length=6,
                                    widget=forms.PasswordInput(attrs={'class':'inputtext', 'placeholder':'再输入一次新密码'}))
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password','')
        if old_password =='':
            raise forms.ValidationError('你没有原密码吗？')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('你记不住原密码吗？')
        return old_password

    def clean_new_password_check(self):
        new_password = self.cleaned_data['new_password']
        new_password_check = self.cleaned_data['new_password_check']
        if new_password != new_password_check:
            raise forms.ValidationError('两次输入的密码不一致')
        if new_password =='':
            raise forms.ValidationError('你在想啥子')
        return new_password_check 


class BindEmailForm(forms.Form):
    verification_code = forms.CharField(
            label='验证码',
            required = False,
            max_length=20,
            widget=forms.TextInput(attrs={'class':'ver_code', 'placeholder':'邮件内的验证码'})
        )
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

    def clean(self):
    # 判断验证码
        code = self.request.session.get('ver_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

class ForgotPasswordForm(forms.Form):
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'inputtext inputtexta', 'placeholder':'输入验证码'}
        )
    )
    new_password = forms.CharField(
        label='新的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'inputtext inputtexta', 'placeholder':'请输入新的密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)


    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')

        # 判断验证码
        code = self.request.session.get('forgot_password_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return verification_code