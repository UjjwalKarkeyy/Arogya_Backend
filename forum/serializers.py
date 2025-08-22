from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Discussion, Reply, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post_count = serializers.ReadOnlyField()
    
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location', 'website', 'joined_date', 'post_count']


class CategorySerializer(serializers.ModelSerializer):
    discussion_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'discussion_count']
    
    def get_discussion_count(self, obj):
        return obj.discussions.count()


class ReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Reply
        fields = ['id', 'content', 'author', 'created_at', 'updated_at', 'is_solution']
        read_only_fields = ['created_at', 'updated_at']


class DiscussionListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    reply_count = serializers.ReadOnlyField()
    last_reply = ReplySerializer(read_only=True)
    
    class Meta:
        model = Discussion
        fields = ['id', 'title', 'author', 'category', 'created_at', 'updated_at', 
                 'is_pinned', 'is_locked', 'views', 'reply_count', 'last_reply']


class DiscussionDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)
    reply_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Discussion
        fields = ['id', 'title', 'content', 'author', 'category', 'created_at', 
                 'updated_at', 'is_pinned', 'is_locked', 'views', 'replies', 'reply_count']


class DiscussionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = ['title', 'content', 'category']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['content']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['discussion'] = self.context['discussion']
        return super().create(validated_data)
