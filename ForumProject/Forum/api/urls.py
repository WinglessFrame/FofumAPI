from django.contrib import admin
from django.urls import path, include
from .views import PostListAPIView


app_name = 'forum-api'
urlpatterns = [
    path('', PostListAPIView.as_view(), name='post-list')
]