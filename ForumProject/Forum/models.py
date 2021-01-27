from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=256, null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    is_published = models.BooleanField(default=False, null=False, blank=False)
    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)

    def __str__(self):
        return self.title[:20]

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment(MPTTModel):
    text = models.TextField(null=False, blank=False)
    author = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    related_to = models.ForeignKey(Post, blank=False, null=True, on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)

    def __str__(self):
        if self.is_root_node():
            return f"{self.related_to.pk}/Root comment {self.pk}"
        else:
            return f'{self.parent}/{self.pk}'

    #
    # class MPTTMeta:
    #     order_insertion_by = likeCounter #TODO
