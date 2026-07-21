from django.contrib import admin

# Register your models here.
from .models import Person, PersonDetail, Product, ProductDetail, Topic, Entry, PersonHonorSkill

admin.site.register(Person)
admin.site.register(PersonDetail)
admin.site.register(PersonHonorSkill)
admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(Topic)
admin.site.register(Entry)