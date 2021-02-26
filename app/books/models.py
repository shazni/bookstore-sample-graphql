from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    publisher_book_url = models.URLField()
    released_on = models.DateTimeField(auto_now_add=True)
    posted_user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
