from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Category, Discussion, Reply, UserProfile
from .serializers import (
    CategorySerializer, DiscussionListSerializer, DiscussionDetailSerializer,
    DiscussionCreateSerializer, ReplySerializer, ReplyCreateSerializer,
    UserProfileSerializer, UserSerializer
)


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DiscussionListView(generics.ListCreateAPIView):
    queryset = Discussion.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DiscussionCreateSerializer
        return DiscussionListSerializer
    
    def get_queryset(self):
        queryset = Discussion.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__id=category)
        return queryset


class DiscussionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discussion.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        return DiscussionDetailSerializer
    
    def get_object(self):
        obj = super().get_object()
        # Increment view count
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj
    
    def update(self, request, *args, **kwargs):
        discussion = self.get_object()
        if discussion.author != request.user:
            return Response(
                {'error': 'You can only edit your own discussions'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        discussion = self.get_object()
        if discussion.author != request.user:
            return Response(
                {'error': 'You can only delete your own discussions'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class ReplyListCreateView(generics.ListCreateAPIView):
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        discussion_id = self.kwargs['discussion_id']
        return Reply.objects.filter(discussion_id=discussion_id)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReplyCreateSerializer
        return ReplySerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        discussion_id = self.kwargs['discussion_id']
        context['discussion'] = get_object_or_404(Discussion, id=discussion_id)
        return context


class ReplyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def update(self, request, *args, **kwargs):
        reply = self.get_object()
        if reply.author != request.user:
            return Response(
                {'error': 'You can only edit your own replies'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        reply = self.get_object()
        if reply.author != request.user:
            return Response(
                {'error': 'You can only delete your own replies'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.user != request.user:
            return Response(
                {'error': 'You can only edit your own profile'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
