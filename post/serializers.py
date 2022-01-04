from rest_framework import serializers

from .models import Post, PostMedia

class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model= PostMedia
        fields= ["id", "img", "post"]


class PostCreateSerializer(serializers.ModelSerializer):
    post_media= PostMediaSerializer(many= True)

    class Meta:
        model= Post
        fields= ["id", "post_media", "user", "caption", "date_posted"]
