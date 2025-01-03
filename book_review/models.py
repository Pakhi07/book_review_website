from django.contrib.auth.models import User
from django.db import models
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_genre = models.CharField(max_length=100, blank=True)
    favorite_author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
class Book(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # or use IntegerField if it's an integer

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.CharField(default='Unknown Author', max_length=255)
    rating = models.IntegerField()  # Rating out of 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title}"

class Bookshelf(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return f"{self.user.username}'s Bookshelf"
