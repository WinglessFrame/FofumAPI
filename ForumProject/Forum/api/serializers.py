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


class PostListSerializer(serializers.ModelSerializer):
    like_counter = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.title

    def get_like_counter(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        if obj.comments.count() == 0:
            return 0
        else:
            comments = obj.comments.all()
            total = 0
            for parent_comment in comments:
                comment_family = parent_comment.get_family()
                total += comment_family.count()
            return total

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
    dislike_counter = serializers.SerializerMethodField()
    like_dislike_status = serializers.SerializerMethodField()
    like_unlike_url = serializers.SerializerMethodField()
    dislike_undislike_url = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()

    def get_like_counter(self, obj):
        return obj.likes.count()

    def get_dislike_counter(self, obj):
        return obj.dislikes.count()

    def get_like_unlike_url(self, obj):
        request = self.context.get('request')
        if request.user in obj.dislikes.all():
            return "Undislike post first"
        return reverse('forum-api:post-like', args=[obj.pk], request=request)

    def get_dislike_undislike_url(self, obj):
        request = self.context.get('request')
        if request.user in obj.likes.all():
            return "Unlike post first"
        return reverse('forum-api:post-dislike', args=[obj.pk], request=request)

    def get_like_dislike_status(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            status = obj in user.post_likes.all()
            if status:
                return "liked"
            else:
                status = obj in user.post_dislikes.all()
                if status:
                    return "disliked"
                else:
                    return "not-rated"
        else:
            return "Requires authentication"

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
            'dislike_counter',
            'like_dislike_status',
            'like_unlike_url',
            'dislike_undislike_url',
            'comments',
        )
