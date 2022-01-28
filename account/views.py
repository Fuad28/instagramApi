from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import AllowAny,  IsAdminUser, IsAuthenticated,  IsAuthenticatedOrReadOnly
from rest_framework.filters  import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

from post.models import Post
from post.serializers import PostSerializer
from.serializers import UserCreateSerializer, SimpleUserSerializer, FollowRelationsSerializer
from .models  import FollowRelations
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


class FollowRelationsView(ViewSet):

    queryset= FollowRelations.objects.all()
    serializer_class= FollowRelationsSerializer

    def current_user(self):
        # return get_object_or_404(User.objects.get(id= request.user.id))
        return get_object_or_404(User.objects.filter(id= 1))
        
    def other_user(self, username):
        return get_object_or_404(User.objects.filter(username= username))

    def get(self, request, *args, **kwargs):
        # queryset=FollowRelations.objects.prefetch_related(
        #     "followers", 'following', 'pending', 'blocked').filter(
        #         user_id= User.objects.get(username=self.kwargs["user_username"]).id)
        queryset=FollowRelations.objects.prefetch_related("followers", 'following', 'pending', 'blocked').filter(user_id= 1)
        serializer= FollowRelationsSerializer(queryset, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)

    def follow(self, request, *args, **kwargs):
        current_user= self.current_user()
        other_user= self.other_user(kwargs["username"])

        if other_user.private:
            #send request by adding to pending list
            pend= FollowRelations.objects.get_or_create(user_id= other_user.id).pending.add(current_user)
            serializer= FollowRelationsSerializer(pend)
            serializer.is_valid(raise_exception= True)
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK) #{"Follow request: Follow request sent"}

        elif other_user.blocked_user.filter(id= current_user.id).exists():
            return Response({"Follow failed: You can't follow this user"}, status= status.HTTP_401_UNAUTHORIZED)
        
        following= current_user.following.add(other_user) ##FollowRelations.objects.get_or_create(user_id= self.kwargs["users_pk"])
        follower= other_user.followers.add(current_user)
        serializer1= FollowRelationsSerializer(following)
        serializer1.is_valid(raise_exception= True)
        serializer1.save()

        serializer2= FollowRelationsSerializer(follower)
        serializer2.is_valid(raise_exception= True)
        serializer2.save()
        
        return Response(serializer1.data, status= status.HTTP_200_OK) #{"Following" : "Following success!!"}



