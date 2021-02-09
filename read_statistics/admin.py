from django.contrib import admin
from .models import ReadNum,ReadDetail
# Register your models here.

@admin.register(ReadNum)
class ReadNum_Admin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object','object_id')

@admin.register(ReadDetail)
class ReadDetail_Admin(admin.ModelAdmin):
    list_display = ('date', 'read_num', 'content_object','object_id')