from django.shortcuts import render
from django.shortcuts import get_object_or_404 

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import  ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser


from .serializers import PostSerializer, PostCommentSerializer, CommentReplySerializer
from  .permissions import  IsUserOrAdminUser
from .models import Post, PostComment, CommentReply

class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related('user').all()
    serializer_class= PostSerializer
    parser_classes = [MultiPartParser, FormParser]
    # permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}

    # def get_permissions(self):
    #     if self.request.method in ["PATCH", "DELETE", "PUT"]:
    #         return  [IsUserOrAdminUser()]

    #     elif self.request.method == "POST":
    #         return [IsAuthenticated()]

    #     return [AllowAny()]

class PostCommentsViewSet(ModelViewSet):
    serializer_class = PostCommentSerializer

    def get_serializer_context(self):
        return {"request": self.request,  "post_pk": self.kwargs["post_pk"]}

    def get_queryset(self):
        return PostComment.objects.select_related("user", "post").filter(post_id= self.kwargs["post_pk"])

class CommentReplyViewSet(ModelViewSet):
    serializer_class = CommentReplySerializer

    def get_serializer_context(self):
        return {"request": self.request, "comment_pk": self.kwargs['comment_pk'], "post_pk": self.kwargs['post_pk']}

    def get_queryset(self):
        return CommentReply.objects.select_related("user", "comment").filter(comment_id= self.kwargs['comment_pk'])
