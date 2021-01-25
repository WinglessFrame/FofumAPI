from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import authentication

from ..models import Post
from .serializers import PostSerializer, PostDetailSerializer


class PostListAPIView(ListCreateAPIView):
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = []
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_published=True)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = []
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'
    queryset = Post.objects.filter(is_published=True)


class PostLikeView(APIView):
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        print(request.user)
        if request.user.is_authenticated:
            return Response(data={'You can like'}, status=200)
        else:
            return Response(data={'You are not allowed to like'}, status=400)