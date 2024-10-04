from django.shortcuts import render
from django.db.models import Count, Q
from .models import Book, Author, Genre

def book_list(request):
    complex_books = Book.objects.filter(
        author__name='Hoài Nam', 
        published_date__gt='2021-01-01',
        genre__name='Khoa Học Viễn Tưởng'
    )

    or_condition_books = Book.objects.filter(
        Q(title__icontains='Hành Trình') | Q(author__name='Nam ne'),
        published_date__gt='2015-01-01'
    )

    genre_counts = Genre.objects.annotate(total_books=Count('book')).order_by('-total_books')

    author_stats = Author.objects.annotate(total_books=Count('book')).filter(total_books__gt=1)

    latest_books_by_genre = Book.objects.filter(genre__isnull=False).order_by('genre', '-published_date')

    all_books = Book.objects.prefetch_related('author', 'genre')

    context = {
        'complex_books': complex_books,
        'or_condition_books': or_condition_books,
        'genre_counts': genre_counts,
        'author_stats': author_stats,
        'latest_books_by_genre': latest_books_by_genre,
        'all_books': all_books,
    }
    
    return render(request, 'books/book_list.html', context)
