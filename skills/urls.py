from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('browse/', views.browse_users, name='browse_users'),
    path('list/', views.skill_list, name='skill_list'),
]