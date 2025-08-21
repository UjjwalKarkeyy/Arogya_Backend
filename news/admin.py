from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import News, Notification, Tag, Category

admin.site.register(Tag)
admin.site.register(News)
admin.site.register(Notification)
admin.site.register(Category)

