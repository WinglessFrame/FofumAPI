from django.contrib import admin
from .models import Post, Category, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'is_published', 'text', 'category')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'related_to', 'parent')


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
