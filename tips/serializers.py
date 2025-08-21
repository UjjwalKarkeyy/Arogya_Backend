from rest_framework import serializers
from .models import Tip


class TipSerializer(serializers.ModelSerializer):
    """Serializer for Tip model"""

    class Meta:
        model = Tip
        fields = ['id', 'title', 'content', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value.strip()

    def validate_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters long.")
        return value.strip()


class TipCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tips"""
    
    class Meta:
        model = Tip
        fields = ['title', 'content', 'is_active']

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value.strip()

    def validate_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters long.")
        return value.strip()