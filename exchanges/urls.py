from django.urls import path
from . import views

app_name = 'exchanges'

urlpatterns = [
    path('send/<str:username>/', views.send_request, name='send_request'),
    path('detail/<int:pk>/', views.request_detail, name='request_detail'),
    path('accept/<int:pk>/', views.accept_request, name='accept_request'),
    path('decline/<int:pk>/', views.decline_request, name='decline_request'),
    path('complete/<int:pk>/', views.complete_request, name='complete_request'),
    path('cancel/<int:pk>/', views.cancel_request, name='cancel_request'),
    path('my-exchanges/', views.my_exchanges, name='my_exchanges'),
]