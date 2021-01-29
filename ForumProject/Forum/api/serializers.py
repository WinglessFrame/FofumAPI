from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

from ..models import Post, Comment

User = get_user_model()


# COMMENT SERIALIZERS
class CommentSerializer(serializers.ModelSerializer):
    related_comments = serializers.SerializerMethodField()
    like_dislike_status = serializers.SerializerMethodField()
    like_unlike_url = serializers.SerializerMethodField()
    dislike_undislike_url = serializers.SerializerMethodField()
    like_counter = serializers.SerializerMethodField()
    dislike_counter = serializers.SerializerMethodField()
    change = serializers.SerializerMethodField()
    to_comment = serializers.SerializerMethodField()

    def get_to_comment(self, obj):
        request = self.context.get('request')
        related_to = self.context.get('related_to')
        return reverse('forum-api:comment-comment', args=[related_to, obj.pk], request=request)

    def get_change(self, obj):
        request = self.context.get('request')
        if request.user == obj.author:
            return reverse('forum-api:comment-detail', args=[obj.pk], request=request)
        else:
            return "Forbidden"

    def get_like_counter(self, obj):
        return obj.likes.count()

    def get_dislike_counter(self, obj):
        return obj.dislikes.count()

    def get_related_comments(self, obj):
        if not obj.is_leaf_node():
            children = obj.get_children()
            serialized = CommentSerializer(children, many=True, context=self.context)
            return serialized.data
        else:
            return []

    def get_dislike_undislike_url(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return "Authorization required"
        if obj in request.user.comment_likes.all():
            return "Unlike post first"
        return reverse('forum-api:comment-dislike', args=[obj.pk], request=request)

    def get_like_unlike_url(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return "Authorization required"
        if obj in request.user.comment_dislikes.all():
            return "Undislike post first"
        return reverse('forum-api:comment-like', args=[obj.pk], request=request)

    def get_like_dislike_status(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return "Authorization required"
        if user.is_authenticated:
            status = obj in user.comment_likes.all()
            if status:
                return "liked"
            else:
                status = obj in user.comment_dislikes.all()
                if status:
                    return "disliked"
                else:
                    return "not-rated"
        else:
            return "Requires authentication"

    class Meta:
        model = Comment
        fields = (
            'author',
            'text',
            'created_at',
            'updated_at',
            'like_counter',
            'dislike_counter',
            'like_dislike_status',
            'like_unlike_url',
            'dislike_undislike_url',
            'change',
            'to_comment',
            'related_comments',
        )


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'text',
        )


# POST SERIALIZERS
class PostListSerializer(serializers.ModelSerializer):
    like_counter = serializers.SerializerMethodField()
    dislike_counter = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()

    def get_like_counter(self, obj):
        return obj.likes.count()

    def get_dislike_counter(self, obj):
        return obj.dislikes.count()

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
            'dislike_counter',
            'comments_count',
            'detail',
        )


class PostDetailSerializer(serializers.ModelSerializer):
    like_counter = serializers.SerializerMethodField()
    dislike_counter = serializers.SerializerMethodField()
    like_dislike_status = serializers.SerializerMethodField()
    like_unlike_url = serializers.SerializerMethodField()
    dislike_undislike_url = serializers.SerializerMethodField()
    to_comment = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    
    def get_to_comment(self, obj):
        request = self.context.get('request')
        return reverse('forum-api:post-comment', args=[obj.pk], request=request)

    def get_to_comment(self, obj):
        request = self.context.get('request')
        return reverse('forum-api:post-comment', args=[obj.pk], request=request)

    def get_comments(self, obj):
        context = self.context
        objects = obj.comments.all()
        serializer = CommentSerializer(objects, many=True, context=context)
        return serializer.data

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
