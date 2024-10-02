# demo/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/create/', views.create_book, name='create_book'),
    path('book/update/<int:pk>/', views.update_book, name='update_book'),
    path('book/delete/<int:pk>/', views.delete_book, name='delete_book'),
]
