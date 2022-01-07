from django.shortcuts import render

from  rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import  ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser


from .serializers import PostMediaSerializer, PostSerializer
from  .permissions import  IsUserOrAdminUser
from .models import Post, PostMedia

class PostView(ModelViewSet):
    queryset = Post.objects.select_related('user').all()
    serializer_class= PostSerializer
    parser_classes = [MultiPartParser, FormParser]
    # permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE", "PUT"]:
            return  [IsUserOrAdminUser()]

        elif self.request.method == "POST":
            return [IsAuthenticated()]

        return [AllowAny()]