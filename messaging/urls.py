from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('conversation/<int:exchange_id>/', views.conversation_detail, name='conversation_detail'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
]