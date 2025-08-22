from django.contrib import admin
from .models import Category, Discussion, Reply, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at', 'is_pinned', 'is_locked', 'views']
    list_filter = ['category', 'is_pinned', 'is_locked', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['views', 'created_at', 'updated_at']


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['discussion', 'author', 'created_at', 'is_solution']
    list_filter = ['is_solution', 'created_at']
    search_fields = ['content', 'author__username', 'discussion__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'joined_date']
    search_fields = ['user__username', 'location']
    readonly_fields = ['joined_date']
