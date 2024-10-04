from django.shortcuts import render
from .models import Book, Author, Genre
from books import models
from django.db.models import Count

def book_list(request):
    all_books = Book.objects.all()
    specific_books = Book.objects.filter(title__icontains='Hành Trình Đến Vô Tận')
    author_books = Book.objects.filter(author__name='Hoài Nam')
    genre_books = Book.objects.filter(genre__name='Phiêu Lưu')
    author_counts = Author.objects.annotate(num_books=Count('book'))
    recent_books = Book.objects.filter(published_date__year__gt=2020)
    books_with_title_containing = Book.objects.filter(title__icontains='Đến')
    authors_with_multiple_books = Author.objects.annotate(num_books=Count('book')).filter(num_books__gt=1)
    books_by_authors = {author: author.book_set.all() for author in Author.objects.all()}
    books_sorted_by_genre = {genre: genre.book_set.order_by('-published_date') for genre in Genre.objects.all()}
    books_with_genres = Book.objects.filter(genre__isnull=False)
    authors_and_books = Author.objects.prefetch_related('book_set').all()
    
    context = {
        'all_books': all_books,
        'specific_books': specific_books,
        'author_books': author_books,
        'genre_books': genre_books,
        'author_counts': author_counts,
        'recent_books': recent_books,
        'books_with_title_containing': books_with_title_containing,
        'authors_with_multiple_books': authors_with_multiple_books,
        'books_by_authors': books_by_authors,
        'books_sorted_by_genre': books_sorted_by_genre,
        'books_with_genres': books_with_genres,
        'authors_and_books': authors_and_books,
    }

    return render(request, 'books/book_list.html', context)
