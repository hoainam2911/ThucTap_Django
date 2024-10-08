from django.shortcuts import render, redirect
from .models import Contact, Group
from django.core.paginator import Paginator
from django_filters import rest_framework as filters
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
class ContactFilter(filters.FilterSet):
    class Meta:
        model = Contact
        fields = {
            'name': ['icontains'],
            'phone': ['icontains'],
            'email': ['icontains'],
        }

def contact_list(request):
    contact_filter = ContactFilter(request.GET, queryset=Contact.objects.all())
    paginator = Paginator(contact_filter.qs, 10)
    page_number = request.GET.get('page')
    contacts = paginator.get_page(page_number)

    return render(request, 'contacts/contact_list.html', {'filter': contact_filter, 'contacts': contacts})

def add_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        company = request.POST.get('company')

        Contact.objects.create(name=name, phone=phone, email=email, address=address, company=company)
        return redirect('contact_list')

    return render(request, 'contacts/contact_form.html')

def send_email_to_contact(request, id):  # Cập nhật hàm để nhận request và id
    contact = get_object_or_404(Contact, id=id)  # Tìm kiếm contact bằng id
    
    if request.method == 'POST':
        subject = 'Notification from Contacts'
        message = f'Hello {contact.name},\n\nThis is a message from your contacts!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [contact.email]

        send_mail(subject, message, from_email, recipient_list)
        return redirect('contact_list')  # Chuyển hướng sau khi gửi email

    return render(request, 'contacts/send_email.html', {'contact': contact})  # Render form gửi email

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('contact_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('contact_list')
    return render(request, 'registration/login.html')
