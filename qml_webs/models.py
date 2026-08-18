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
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.01, verbose_name="价格(元)")
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_PENDING = 0
    STATUS_PAID = 1
    STATUS_CLOSED = 2
    STATUS_CHOICES = (
        (STATUS_PENDING, "待支付"),
        (STATUS_PAID, "已支付"),
        (STATUS_CLOSED, "已关闭"),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_no = models.CharField(max_length=64, unique=True, verbose_name="商户订单号")
    transaction_id = models.CharField(max_length=64, blank=True, null=True, verbose_name="微信单号")
    total_fee = models.IntegerField(verbose_name="金额(分)")
    status = models.SmallIntegerField(default=STATUS_PENDING, choices=STATUS_CHOICES)
    code_url = models.CharField(max_length=512, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    pay_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "订单"


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