from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import  account
from django.urls import path, include

urlpatterns = [
    # path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path("accounts/", include('account.urls'), name= "accounts"),
    path("posts/", include('post.urls'), name= "posts"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)