from django.contrib import admin
from django.urls import path, include, re_path
from .views import (
    PostListAPIView,
    PostDetailAPIView,
    PostLikeView,
    PostDislikeView,
    CommentDislikeView,
    CommentLikeView,
    CommentDetailView,
    CommentCreateView,
    UserStatisticsView,
)


app_name = 'forum-api'
urlpatterns = [
    path('', PostListAPIView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
    path('<int:pk>/dislike/', PostDislikeView.as_view(), name='post-dislike'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comments/<int:pk>/like/', CommentLikeView.as_view(), name='comment-like'),
    path('comments/<int:pk>/dislike/', CommentDislikeView.as_view(), name='comment-dislike'),
    re_path(r'(?P<post_pk>\d+)/(?P<comment_pk>\d+)/comment/', CommentCreateView.as_view(), name='comment-comment'),
    re_path(r'(?P<post_pk>\d+)/comment/', CommentCreateView.as_view(), name='post-comment'),
    path('users/', UserStatisticsView.as_view(), name='user-stat')
]
