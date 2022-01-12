from pprint import pprint
from django.urls import path

from rest_framework_nested import  routers

from .import views

router= routers.DefaultRouter()
router.register("", views.PostViewSet, basename= "posts")

post_router= routers.NestedSimpleRouter(router, "", lookup= "post")
post_router.register("comments", views.PostCommentsViewSet, basename= "comments")

comment_router= routers.NestedSimpleRouter(post_router, "comments", lookup= "comment")
comment_router.register("replies", views.CommentReplyViewSet, basename= "reply")



urlpatterns= router.urls + post_router.urls + comment_router.urls


