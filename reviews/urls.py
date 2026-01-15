from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:exchange_id>/', views.create_review, name='create_review'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
]