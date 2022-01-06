from rest_framework import serializers

from .models import Post, PostMedia
from account.models import User
from account.serializers import SimpleUserSerializer

class PostMediaSerializer(serializers.ModelSerializer):
    post= serializers.UUIDField(read_only=True)
    class Meta:
        model= PostMedia
        fields= ["id", "media", "post"]

class PostSerializer(serializers.ModelSerializer):
    post_media= PostMediaSerializer()

    class Meta:
        model = Post
        fields= ["id", "user_id", "post_media", "caption"]

    def create(self, validated_data):
        request= self.context["request"]
        post= PostSerializer(data= request.data)
        if post.is_valid(raise_exception=True):
            post= Post.objects.create(user_id= 1, caption=  validated_data["caption"])
            post_media= request.FILES.get("post_media.media") #validated_data["post_media"].get("media")
            for media in post_media:
                    post_media= PostMedia.objects.create(post_id= post.id, media= media)
        
        return post


