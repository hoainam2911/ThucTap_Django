# books/urls.py

from django import views
from django.urls import path
from .views import add_book, book_list, delete_book, edit_book

urlpatterns = [
    path('', book_list, name='book_list'), 
    path('add/', add_book, name='add_book'),
    path('edit/<int:pk>/', edit_book, name='edit_book'),
    path('delete/<int:pk>/',delete_book, name='delete_book'),
]
