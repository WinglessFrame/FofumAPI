from rest_framework import serializers
from ..models import Post


class PostSerializer(serializers.ModelSerializer):
    like_counter = serializers.SerializerMethodField()

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
        )
