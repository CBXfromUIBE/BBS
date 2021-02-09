from django.contrib import admin
from .models import Heart_Favor
# Register your models here.
@admin.register(Heart_Favor)
class Heart_Favor_Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content_object','content_type')