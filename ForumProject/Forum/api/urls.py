from django.contrib import admin
from django.urls import path, include
from .views import (
    PostListAPIView,
    PostDetailAPIView,
    CommentLikeView,
)


app_name = 'forum-api'
urlpatterns = [
    path('', PostListAPIView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('<int:pl>/like/', PostDetailAPIView.as_view(), name='post-like'),
]