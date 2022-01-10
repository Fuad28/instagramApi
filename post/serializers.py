from django.conf import settings
from rest_framework import serializers

from .models import Post, PostComment,  CommentReply
from account.serializers import SimpleUserSerializer


class PostSerializer(serializers.ModelSerializer):
    user= serializers.StringRelatedField()
    class Meta:
        model = Post
        fields= ["id", "user", "media", "caption"]

    def create(self, validated_data):
        request= self.context["request"]
        post= PostSerializer(data= request.data)
        if post.is_valid(raise_exception=True):
            post= Post.objects.create(user_id= request.user.id, caption=  validated_data["caption"], media= validated_data["media"])
        
        return post

class PostCommentSerializer(serializers.ModelSerializer):
    user=  serializers.HyperlinkedRelatedField(view_name= "users-detail", read_only= True, lookup_field= "username")
    post= serializers.HyperlinkedRelatedField(view_name= "posts-detail", read_only= True)
    class Meta:
        model= PostComment
        fields= ["id", "user","post", "comment"]

    def save(self, *args, **kwargs):
        post_pk= self.context["post_pk"]
        # user_id= self.context["request"].user.id
        if Post.objects.filter(id= post_pk).exists():
            self.instance= PostComment.objects.create(post_id=post_pk, user_id= 1, **self.validated_data)
            return  self.instance
           
        else:
            raise serializers.ValidationError("No post with the given id was found")

class CommentReplySerializer(serializers.ModelSerializer):
    user= serializers.HyperlinkedRelatedField(view_name= "users-detail", read_only= True, lookup_field= "username")
    comment= serializers.HyperlinkedRelatedField(view_name= "post-comments-detail", read_only= True)

    class Meta:
        model = CommentReply
        fields = ["id", "user", "comment", "reply"]
            










# class PostMediaSerializer(serializers.ModelSerializer):
#     post= serializers.HyperlinkedRelatedField(view_name= "postsample-detail", read_only= True)
#     class Meta:
#         model= PostMedia
#         fields= ["id", "media", "post"]

# class PostSampleSerializer(serializers.ModelSerializer):
#     user= serializers.ReadOnlyField(source='user.username')
#     media = PostMediaSerializer(source='postmedia_set', many=True)
#     class Meta:
#         model = PostSample
#         fields= ["id", "user", "media", "caption"]

#     def create(self, validated_data):
#         request= self.context["request"]
#         post= PostSampleSerializer(data= request.data)
#         if post.is_valid(raise_exception=True):
#             post= PostSample.objects.create(user_id= 1, caption=  validated_data["caption"])
#             post_media= request.FILES.get("post_media.media") #validated_data["post_media"].get("media")
#             for media in post_media:
#                 post_media_serializer= PostMediaSerializer(data=  {"post":post, "media":media})
#                 if post_media_serializer.is_valid(raise_exception=True):
#                     post_media= PostMedia.objects.create(post_id= post.id, media= media)
        
#         return post