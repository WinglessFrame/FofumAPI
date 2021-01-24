from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Post
from .serializers import PostSerializer


class PostListAPIView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = []
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_published=True)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]