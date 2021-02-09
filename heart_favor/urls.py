from django.urls import path
from . import views

urlpatterns = [
    path('heart_change/',views.heart_change,name='heart_change'),
    path('favor_change/',views.favor_change,name='favor_change'),
]
