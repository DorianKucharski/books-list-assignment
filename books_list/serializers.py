from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    authors = serializers.CharField(max_length=100)
    publish_date = serializers.CharField(max_length=100)
    isbn = serializers.IntegerField()
    page_count = serializers.IntegerField()
    thumbnail = serializers.CharField(max_length=999)
    language = serializers.CharField(max_length=100)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.authors = validated_data.get('authors')
        instance.publish_date = validated_data.get('publish_date')
        instance.isbn = validated_data.get('isbn')
        instance.page_count = validated_data.get('page_count')
        instance.thumbnail = validated_data.get('thumbnail')
        instance.language = validated_data.get('language')
        instance.save()
        return instance

    def create(self, validated_data):
        return Book.objects.create(validated_data)