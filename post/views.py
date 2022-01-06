from django.shortcuts import render

from  rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import  ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import PostMediaSerializer, PostSerializer
from .models import Post, PostMedia

class PostView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class= PostSerializer
    parser_classes = [MultiPartParser, FormParser]
    # permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}