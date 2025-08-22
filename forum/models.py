from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Discussion(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='discussions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-is_pinned', '-updated_at']
    
    def __str__(self):
        return self.title
    
    @property
    def reply_count(self):
        return self.replies.count()
    
    @property
    def last_reply(self):
        return self.replies.order_by('-created_at').first()


class Reply(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_solution = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
        verbose_name_plural = "Replies"
    
    def __str__(self):
        return f"Reply to {self.discussion.title} by {self.author.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='forum_profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Forum Profile"
    
    @property
    def post_count(self):
        return self.user.discussions.count() + self.user.replies.count()
