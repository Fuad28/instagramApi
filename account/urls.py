from django.urls import path

from rest_framework_nested import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

from . import views
from post import  views as post_views 

router= routers.DefaultRouter()
router.register('', views.UsersViewSet, basename= "users")

#follow endpoints
# user_follow= routers.NestedDefaultRouter(router, "", lookup= "users")
# user_follow.register('follow', views.FollowRelationsView, basename= "user-follow")

#to implement the comment and reply endpoints without rewritting 
users_post= routers.NestedDefaultRouter(router, "", lookup= "users")
users_post.register('posts', post_views.UsersPostsViewSet, basename= "users-post")

post_router= routers.NestedSimpleRouter(users_post, 'posts', lookup= "post")
post_router.register("comments", post_views.PostCommentsViewSet, basename= "comments")

comment_router= routers.NestedSimpleRouter(post_router, "comments", lookup= "comment")
comment_router.register("replies", post_views.CommentReplyViewSet, basename= "reply")



urlpatterns = router.urls + users_post.urls + post_router.urls + comment_router.urls +  [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('follow/<str:username>/', views.FollowRelationsView.as_view({"post": "follow"}), name= "follow"),
    path('unfollow/<str:username>/', views.FollowRelationsView.as_view({"post": "unfollow"}), name= "unfollow")
]
