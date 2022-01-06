from django.urls import path

from rest_framework_nested import  routers

from .import views

# router= routers.DefaultRouter()

# router.register("new_post", views.PostView, basename= "new_post")

# urlpatterns= router.urls


urlpatterns = [
    path("new_post/", views.PostView.as_view(), name="new_post")
]