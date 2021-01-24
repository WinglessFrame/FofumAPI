from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from ..models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'author',
            'text',
            'created_at',
            'updated_at',
        )

    # def get_author(self):
    #     return self.author.username


class PostSerializer(serializers.ModelSerializer):
    like_counter = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    # #serializers.PrimaryKeyRelatedField(many=True, source='comments', queryset=Comment.objects.all())

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
            # 'comment_list',
        )
