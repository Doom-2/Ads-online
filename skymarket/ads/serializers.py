from rest_framework import serializers
from .models import Ad, Comment


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['pk', 'title', 'price', 'description', 'image']


class AdDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = [
            'pk', 'title', 'price', 'phone', 'description',
            'author_first_name', 'author_last_name', 'author_id', 'image',
        ]


class AdsByUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['pk', 'title', 'price', 'description', 'image']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'pk', 'text', 'author_id', 'created_at',
            'author_first_name', 'author_last_name', 'ad_id', 'author_image'
        ]
