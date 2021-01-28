from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import authentication
from django.shortcuts import redirect

from ..models import Post, Comment
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentDetailSerializer,
)
from .permissions import IsAuthorOrReadOnly


# POSTS VIEWS
class PostListAPIView(ListCreateAPIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostListSerializer
    queryset = Post.objects.filter(is_published=True)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [IsAuthorOrReadOnly]
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
            return Response(data={'Requires authorization'}, status=403)


class PostDislikeView(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user
        if user.is_authenticated and post:
            if post in request.user.post_dislikes.all():
                user.post_dislikes.remove(post)
                return redirect('forum-api:post-detail', pk=pk)
            else:
                user.post_dislikes.add(post)
                return redirect('forum-api:post-detail', pk=pk)
        else:
            return Response(data={'Requires authorization'}, status=403)


# COMMENTS VIEW
class CommentLikeView(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        user = request.user
        if user.is_authenticated and comment:
            related_to = comment.related_to.pk
            if comment in request.user.comment_likes.all():
                user.comment_likes.remove(comment)
                return redirect('forum-api:post-detail', pk=related_to)
            else:
                user.comment_likes.add(comment)
                return redirect('forum-api:post-detail', pk=related_to)
        else:
            return Response(data={'Requires authorization'}, status=403)


class CommentDislikeView(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        user = request.user
        if user.is_authenticated and comment:
            related_to = comment.related_to.pk
            if comment in request.user.comment_dislikes.all():
                user.comment_dislikes.remove(comment)
                return redirect('forum-api:post-detail', pk=related_to)
            else:
                user.comment_dislikes.add(comment)
                return redirect('forum-api:post-detail', pk=related_to)
        else:
            return Response(data={'Requires authorization'}, status=403)


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentDetailSerializer
    lookup_field = 'pk'
    queryset = Comment.objects.all()


class CommentCreateView(CreateAPIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentDetailSerializer

    def post(self, request, *args, **kwargs):
        post_pk = kwargs.get('post_pk', None)
        comment_pk = kwargs.get('comment_pk', None)
        if comment_pk:
            parent = Comment.objects.get(pk=comment_pk)
        else:
            parent = False
        text = request.POST.get('text', None)
        if not text:
            return Response({'message': 'text required'}, status=403)
        author = request.user
        related_to = Post.objects.get(pk=post_pk)
        if not related_to:
            return Response({'message': 'Post doesnt exist'}, status=404)
        if parent:
            obj = Comment.objects.create(text=text, author=author, related_to=related_to, parent=parent)
        else:
            obj = Comment.objects.create(text=text, author=author, related_to=related_to)
        return redirect('forum-api:post-detail', pk=post_pk)
