from rest_framework import serializers

from .models import Post, Images

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model= Images
        fields= ["id", "img"]