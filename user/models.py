from django.db import models
from django.contrib.auth.models import User

class custom_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name='昵称')
    nickname = models.CharField(max_length=20,default='')
    is_UIBEr = models.BooleanField(default=True)

    def __str__(self):
        return '<custom_user %s for %s>' % (self.nickname,self.user.username)

def get_nickname(self):
    if custom_user.objects.filter(user=self).exists():
        new_user = custom_user.objects.get(user=self)
        return new_user.nickname
    else:
        return ''
def has_nickname(self):
    return custom_user.objects.filter(user=self).exists()

User.get_nickname = get_nickname
User.has_nickname = has_nickname