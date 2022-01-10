from pprint import pprint
from django.urls import path

from rest_framework_nested import  routers

from .import views

router= routers.DefaultRouter()
router.register("", views.PostViewSet, basename= "posts")

comments_router= routers.NestedDefaultRouter(router, "", lookup= "post")
comments_router.register("comments", views.PostCommentsViewSet, basename= "post-comments")



urlpatterns= router.urls + comments_router.urls