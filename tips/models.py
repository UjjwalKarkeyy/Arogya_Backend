from django.db import models
from django.utils import timezone


# class Category(models.Model):
#     """Model for health tip categories"""
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True)
#     icon = models.CharField(max_length=50, blank=True)  # For icon name/path
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name_plural = "Categories"
#         ordering = ['name']

#     def __str__(self):
#         return self.name


class Tip(models.Model):
    """Model for health tips"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    # # category = models.ForeignKey(
    # #     Category, 
    # #     on_delete=models.CASCADE, 
    # #     related_name='tips',
    # #     null=True,
    # #     blank=True
    # )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title