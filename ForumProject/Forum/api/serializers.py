from rest_framework import serializers

from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from ..models import Post, Comment


User = get_user_model()



class CommentSerializer(serializers.ModelSerializer):
    related_comments = serializers.SerializerMethodField()

    def get_related_comments(self, obj):
        if not obj.is_leaf_node():
            children = obj.get_children()
            serialized = CommentSerializer(children, many=True)
            return serialized.data
        else:
            return []

    class Meta:
        model = Comment
        fields = (
            'author',
            'text',
            'created_at',
            'updated_at',
            'related_comments',
        )


class PostSerializer(serializers.ModelSerializer):
    like_counter = serializers.SerializerMethodField()

    comments_count = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.title

    def get_like_counter(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_detail(self, obj):
        request = self.context.get('request')
        return reverse('forum-api:post-detail', args=[obj.pk], request=request)

    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'category',
            'author',
            'created_at',
            'updated_at',
            'like_counter',
            'comments_count',
            'detail',
        )


class PostDetailSerializer(serializers.ModelSerializer):
    like_counter = serializers.SerializerMethodField()
    like_status = serializers.SerializerMethodField()
    like_url = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.title

    def get_like_counter(self, obj):
        return obj.likes.count()

    def get_like_url(self, obj):
        request = self.context.get('request')
        return reverse('forum-api:post-like', args=[obj.pk], request=request)

    def get_like_status(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            status = (obj in user.post_likes.all())
            return status
        else: return "Requires authentication"


    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'category',
            'author',
            'created_at',
            'updated_at',
            'like_counter',

            'like_status',
            'like_url',
        )