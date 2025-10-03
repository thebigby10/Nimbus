from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'file_shareapp'

urlpatterns = [
    path('public-view/', views.public_view, name="public_view"),
    path('file/<uuid:file_id>', views.file_detail, name="file_detail_view"),
    path('download/<uuid:file_id>', views.file_download, name="file_download_view"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('auth-view/',views.auth_view , name="auth_view"),
    # path('files/', views.file_list, name='file_list', ),
]
