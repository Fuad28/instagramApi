from django.urls import path

from rest_framework_nested import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

from . import views

router= routers.DefaultRouter()
router.register('users', views.UsersViewSet, basename= "users")


urlpatterns = router.urls + [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
