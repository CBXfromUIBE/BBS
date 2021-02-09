from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name="user_login"),
    path('login_for_medal/',views.login_for_medal,name='login_for_medal'),
    path('register/', views.user_register, name="user_register"),
    path('forget_pwd/',views.forget_pwd,name='forget_pwd'),
    path('user_logout/', views.user_logout,name="user_logout"),
    path('user_info/', views.user_info,name="user_info"),
    path('change_userinfo/', views.change_userinfo,name="change_userinfo"),
    path('send_verification_code/', views.send_verification_code,name="send_verification_code"),
    path('change_password/', views.change_password,name="change_password"),
    path('update_tiezi/',views.update_tiezi,name="update_tiezi"),
    path('manage_tiezi/',views.manage_tiezi,name="manage_tiezi"),
    path('manage_comment/',views.manage_comment,name="manage_comment"),
    path('manage_heart_user/',views.manage_heart_user,name="manage_heart_user"),
    path('manage_favor_tiezi/',views.manage_favor_tiezi,name="manage_favor_tiezi"),
    path('del_tiezi/<int:tiezi_id>/',views.del_tiezi,name="del_tiezi"),
    path('del_comment/<int:comment_id>/',views.del_comment,name="del_comment"),
    path('get_ta_tiezi_all/<int:ta_id>',views.get_ta_tiezi_all,name="get_ta_tiezi_all"),
    path('cancel_heart/<int:ta_id>',views.cancel_heart,name="cancel_heart"),
    path('cancel_favor/<int:tiezi_id>',views.cancel_favor,name="cancel_favor"),
]
