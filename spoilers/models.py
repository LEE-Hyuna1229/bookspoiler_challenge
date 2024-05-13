from django.db import models
from users.models import User
from books.models import Book

# Create your models here.
class Spoiler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    writer = models.CharField(max_length=225) 
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)