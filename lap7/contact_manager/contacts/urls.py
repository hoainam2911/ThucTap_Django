from django.urls import path
from .views import contact_list, add_contact, send_email_to_contact, register, login_view

urlpatterns = [
    path('', contact_list, name='contact_list'),
    path('add/', add_contact, name='add_contact'),
    path('send_email/<int:id>/', send_email_to_contact, name='send_email'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
]
