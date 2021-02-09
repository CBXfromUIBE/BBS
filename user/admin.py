from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import custom_user


class custom_userInline(admin.StackedInline):
    model = custom_user
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (custom_userInline, )
    list_display = ('username', 'nickname', 'email','is_UIBEr', 'is_staff', 'is_active', 'is_superuser')

    def nickname(self, obj):
        return obj.custom_user.nickname
    nickname.short_description = '昵称'

    def is_UIBEr(self, obj):
        return obj.custom_user.is_UIBEr
    is_UIBEr.short_description = '校内人士'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(custom_user)
class custome_userAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname','is_UIBEr')