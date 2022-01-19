from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,  IsAdminUser, IsAuthenticated,  IsAuthenticatedOrReadOnly
from rest_framework.filters  import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

from post.models import Post
from post.serializers import PostSerializer
from.serializers import UserCreateSerializer, SimpleUserSerializer
from .pagination import DefaultPagination
from .permissions import IsUserOrAdminUser

User= get_user_model()
 
class UsersViewSet(ModelViewSet):
    queryset= User.objects.all()
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    pagination_class= DefaultPagination
    filter_backends= [DjangoFilterBackend]
    filterset_fields= ["username", "first_name", "last_name"] 

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST' or (isinstance(self.get_permissions()[0], IsUserOrAdminUser)):
            return UserCreateSerializer
        return SimpleUserSerializer
    
    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE", "PUT"]:
            return  [IsUserOrAdminUser()]
        return [AllowAny()]