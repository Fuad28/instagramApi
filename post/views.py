from django.shortcuts import render

from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.viewsets import  ModelViewSet

from .serializers import PostMediaSerializer, PostCreateSerializer
from .models import Post

class PostCreateView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class= PostCreateSerializer

    def create(self, request, *args, **kwargs):
        post_data= PostCreateSerializer(data= request.data)
        if post_data.is_valid(raise_exception=True):
            media_data= request.FIles.getlist("files")
            for media in media_data:
                post_media= PostMediaSerializer(data= {"post": post_data, "media": media})
                if post_media.is_valid(raise_exception=True):
                    post_media.save()
            
            serializer= post_data.save()
            return(serializer.data)




