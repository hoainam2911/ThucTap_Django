from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class BookManager(models.Manager):
    def available_books(self):
        return self.filter(available=True)

    def borrowed_books(self):
        return self.filter(available=False)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    published_date = models.DateField(default=timezone.now)
    isbn = models.CharField(max_length=13, unique=True)
    available = models.BooleanField(default=True)

    objects = BookManager()

    def mark_borrowed(self):
        self.available = False
        self.save()

    def mark_returned(self):
        self.available = True
        self.save()

    def __str__(self):
        return f"{self.title} by {self.author.name}"

@receiver(pre_save, sender=Book)
def pre_save_book(sender, instance, **kwargs):
    print(f"Preparing to save: {instance.title}")

@receiver(post_save, sender=Book)
def post_save_book(sender, instance, created, **kwargs):
    if created:
        print(f"Book created: {instance.title}")
    else:
        print(f"Book updated: {instance.title}")
