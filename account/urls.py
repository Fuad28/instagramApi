from django.urls import path

from rest_framework_nested import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

from . import views
from post import  views as post_views 

router= routers.DefaultRouter()
router.register('', views.UsersViewSet, basename= "users")

#followrequest endpoints
# follow_request= routers.NestedDefaultRouter(router, "", lookup= "users")
# follow_request.register('pending', views.FollowRequestViewSet, basename= "follow-request")

#to implement the comment and reply endpoints without rewritting 
users_post= routers.NestedDefaultRouter(router, "", lookup= "users")
users_post.register('posts', post_views.UsersPostsViewSet, basename= "users-post")

post_router= routers.NestedSimpleRouter(users_post, 'posts', lookup= "post")
post_router.register("comments", post_views.PostCommentsViewSet, basename= "comments")

comment_router= routers.NestedSimpleRouter(post_router, "comments", lookup= "comment")
comment_router.register("replies", post_views.CommentReplyViewSet, basename= "reply")



urlpatterns =[
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('pending/', views.FollowRequestViewSet.as_view({'get': 'list'}), name= "follow-request"),
    path('pending/<int:pk>', views.FollowRequestViewSet.as_view({'get': 'details'}), name= "follow-request-detail"),
    path('pending/<int:pk>/accept/', views.FollowRequestViewSet.as_view({'get': 'accept'}), name= "follow-request-accept"),
    path('pending/<int:pk>/reject/', views.FollowRequestViewSet.as_view({'get': 'reject'}), name= "follow-request-reject"),
    ] + router.urls + users_post.urls + post_router.urls + comment_router.urls