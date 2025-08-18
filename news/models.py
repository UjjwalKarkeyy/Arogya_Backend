from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='news', blank=True)  # Tag is defined above
    category = models.ManyToManyField(Category, related_name='news', blank=True)  # Category is defined above

    def __str__(self):
        return self.title

class Notification(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='notifications')
    # news_title = models.CharField(max_length=255, null=True, blank=True)
    # news_content = models.TextField(null=True, blank=True)
    # news_category = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.news.title

from django.db.models.signals import post_save
from django.dispatch import receiver

# @receiver(post_save, sender=News)
# def create_notification_for_news(sender, instance, created, **kwargs):
#     if created:
#         Notification.objects.create(news=instance)
#         print(f"Notification created for news: {instance.title}")
#         return f"Notification for: {self.news.title}"


