from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=32, blank=False, unique=True)
    username = models.CharField(max_length=16, blank=False, unique=True)
    password = models.CharField(max_length=16, blank=False)

    def __str__(self):
        return self.name


class Story(models.Model):
    author = models.ForeignKey(Author, related_name='story', on_delete=models.CASCADE)
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=16)
    region = models.CharField(max_length=16)
    detail = models.CharField(max_length=512)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.headline
