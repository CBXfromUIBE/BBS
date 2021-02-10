from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNumExpandMethod,ReadDetail
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
class TieZi_Label(models.Model):
    name = models.CharField(u'标签', max_length=20, null=True, blank=True, help_text='不超过20个字符')
    
    def __str__(self):
        return u'%s' % (self.name)

class TieZi(models.Model,ReadNumExpandMethod):
    title = models.CharField(u'帖子标题', max_length=40, help_text='不超过40个字符')
    tiezi_label = models.ForeignKey(TieZi_Label, on_delete=models.CASCADE,blank=True)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_detail = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True,blank=True)
    last_altered_time = models.DateTimeField(auto_now=True,blank=True)
    
    
    def __str__(self):
        return u'%s' % (self.title)

    class Meta:
        ordering = ['-created_time']


        