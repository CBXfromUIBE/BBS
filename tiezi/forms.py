from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import TieZi

class TieZiForm(forms.Form):

    title = forms.CharField(label="起个标题吧",
        max_length=40,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'震惊！一学生竟在图书馆'}))
    text = forms.CharField(label="内容编辑区域",widget=CKEditorWidget(config_name='comment_ckeditor'),
                           error_messages={'required': '发空贴是几个意思？'})
    tiezi_label = forms.ChoiceField(
        label="给帖子加个标签吧",
        choices=[('1','二手交易'),('2','考研保研'),('3','恋爱八卦'),('4','就业创业')],
        widget=forms.widgets.Select())

    

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(TieZiForm, self).__init__(*args, **kwargs)
