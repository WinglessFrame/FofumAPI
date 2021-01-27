from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import authentication
from django.shortcuts import redirect

from ..models import Post
from .serializers import PostSerializer, PostDetailSerializer


class PostListAPIView(ListCreateAPIView):
    authentication_classes  = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes= [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_published=True)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'
    queryset = Post.objects.filter(is_published=True)


class PostLikeView(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user
        if user.is_authenticated and post:
            if post in request.user.post_likes.all():
                user.post_likes.remove(post)
                return redirect('forum-api:post-detail', pk=pk)
            else:
                user.post_likes.add(post)
                return redirect('forum-api:post-detail', pk=pk)
        else:
            return Response(data={'You are not allowed to like'}, status=400)
