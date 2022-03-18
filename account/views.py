from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import AllowAny,  IsAdminUser, IsAuthenticated,  IsAuthenticatedOrReadOnly
from rest_framework.filters  import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

from post.models import Post
from .models import FollowRequest
from post.serializers import PostSerializer
from.serializers import UserCreateSerializer, SimpleUserSerializer, FollowRequestSerializer
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

    def current_user(self):
        return self.request.user
        
    def other_user(self, username):
        return get_object_or_404(User, username= username.title())

    @action(detail= False)
    def followers(self, request, *args, **kwargs):
        queryset= request.user.followers
        print(queryset)
        serializer= SimpleUserSerializer(queryset, many= True, context= {"request": self.request})
        return Response(serializer.data, status= status.HTTP_200_OK)

    @action(detail= False)
    def following(self, request, *args, **kwargs):
        queryset= request.user.following
        serializer= SimpleUserSerializer(queryset, many= True, context= {"request": self.request})
        return Response(serializer.data, status= status.HTTP_200_OK)


    @action(detail=True, methods=['get'])
    def follow(self, request, username= None):
        current_user= self.request.user
        other_user= self.other_user(username)

        if other_user.private:
            #send a follow request
            FollowRequest.objects.create(requester= current_user, to_follow= other_user)
            return Response({"Follow request: Follow request sent"}, status= status.HTTP_200_OK)

        elif current_user not in other_user.followers:
            current_user.follow(other_user)
            return Response({"Following" : "Following success!!"}, status= status.HTTP_200_OK)
        return Response({"Following" : "You follow them already!!"}, status= status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def unfollow(self, request, username= None):
        current_user= self.request.user
        other_user= self.other_user(username)

        if current_user in other_user.followers:
            current_user.unfollow(other_user)
            return Response({"Unfollowing" : "Unfollowing success!!"}, status= status.HTTP_200_OK)
        return Response({"Unfollowing" : "You didn't follow them  before!!"}, status= status.HTTP_200_OK)

    
    @action(detail= False)
    def blocking(self, request, *args, **kwargs):
        queryset= request.user.blocking
        serializer= SimpleUserSerializer(queryset, many= True, context= {"request": self.request})
        return Response(serializer.data, status= status.HTTP_200_OK)


    @action(detail=True, methods=['get'])
    def block(self, request, username= None):
        current_user= self.request.user
        other_user= self.other_user(username)

        if current_user not in other_user.blocking:
            current_user.block(other_user)
            return Response({"Blocking" : "Blocking success!!"}, status= status.HTTP_200_OK)
        return Response({"Blocking" : "You've blocked them already!!"}, status= status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def unblock(self, request, username= None):
        current_user= self.request.user
        other_user= self.other_user(username)

        if current_user in other_user.blocking:
            current_user.unblock(other_user)
            return Response({"Unblocking" : "Unblocking success!!"}, status= status.HTTP_200_OK)
        return Response({"Unblocking" : "You didn't block this user before!!"}, status= status.HTTP_200_OK)


class FollowRequestViewSet(ModelViewSet):
    serializer_class= FollowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FollowRequest.objects.filter(to_follow_id= self.request.user.id)

    def details(self, *args, **kwargs):
        follow_request= FollowRequest.objects.get(id= kwargs.get("pk"))
        serializer= FollowRequestSerializer(follow_request)
        return Response(serializer.data, status= status.HTTP_200_OK)

    def accept(self, request, pk= None, **kwargs):
        follow_request= FollowRequest.objects.get(id= pk)
        follow_request.accept
        follow_request.delete()
        return Response({"Follow Request" : "Request Accepted!!"}, status= status.HTTP_200_OK)

    def reject(self, request, pk= None):
        follow_request= FollowRequest.objects.get(id= pk)
        follow_request.reject
        follow_request.delete()
        return Response({"Follow Request" : "Request Rejected!!"}, status= status.HTTP_200_OK)