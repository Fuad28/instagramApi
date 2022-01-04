from django.urls import path

from rest_framework_nested import  routers

from .import views

router= routers.DefaultRouter()

router.register("new_post", views.PostCreateView, basename= "new_post")


urlpatterns = router.urls