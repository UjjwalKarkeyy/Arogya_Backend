from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Discussions
    path('discussions/', views.DiscussionListView.as_view(), name='discussion-list'),
    path('discussions/<int:pk>/', views.DiscussionDetailView.as_view(), name='discussion-detail'),
    
    # Replies
    path('discussions/<int:discussion_id>/replies/', views.ReplyListCreateView.as_view(), name='reply-list'),
    path('replies/<int:pk>/', views.ReplyDetailView.as_view(), name='reply-detail'),
    
    # User Profiles
    path('profiles/', views.UserProfileListView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', views.UserProfileDetailView.as_view(), name='profile-detail'),
]
