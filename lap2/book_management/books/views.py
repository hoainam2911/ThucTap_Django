# books/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():  # Kiểm tra tính hợp lệ của form
            form.save()  # Lưu sách vào cơ sở dữ liệu
            return redirect('book_list')  # Quay lại danh sách sách
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})  # Trả về template với form

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Quay lại danh sách sách
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form, 'book': book})

# View để xóa sách
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # Quay lại danh sách sách
    return render(request, 'books/delete_book.html', {'book': book})