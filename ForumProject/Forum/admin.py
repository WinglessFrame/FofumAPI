from django.contrib import admin
from .models import Post, Category, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'is_published', 'text', 'category')
    list_editable = ('is_published',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'related_to', 'parent', 'text')



admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
