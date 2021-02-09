from django.urls import path
from . import views

urlpatterns = [
    path('', views.tiezi_list, name='tiezi_list'),
    path('<int:tiezi_id>',views.tiezi_detail, name="tiezi_detail"),
    path('label/<int:label_id>', views.label_to_tiezi, name="label_to_tiezi"),
]
