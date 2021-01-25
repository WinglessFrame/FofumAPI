from rest_framework import serializers

from ..models import Post, Comment


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
    comments = CommentSerializer(many=True, read_only=True)

    def get_root_comments(self):
        all_comments = [obj for obj in self.comments]
        filtered = [obj for obj in all_comments if obj.is_root_node()]
        return filtered

    def get_like_counter(self, obj):
        return obj.get_total_likes()

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
            'comments',
        )
