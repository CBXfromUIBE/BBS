from django.contrib import admin
from .models import TieZi_Label,TieZi
# Register your models here.

@admin.register(TieZi_Label)
class TieZi_Label_Admin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(TieZi)
class Tiezi_Admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'tiezi_label', 'author', 'get_read_num', 'created_time', 'last_altered_time')
    
