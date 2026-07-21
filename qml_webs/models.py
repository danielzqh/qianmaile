from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_joined = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', default='default/default_image.png', blank=True, null=True)
    def __str__(self):
        return self.name


class PersonDetail(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text


class PersonHonorSkill(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='video/', default='default/default_video.mp4', blank=True, null=True)
    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text


class Topic(models.Model):
    '''user interested topic'''
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return f"{self.text[:50]}..."