
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('auth/', include('user_auth.urls'), name='auth'),
    path('file-share/', include('file_shareapp.urls'), name='file-share')
]
