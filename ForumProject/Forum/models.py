from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False)


class Post(models.Model):
    text = models.TextField(null=False, blank=False)
    is_published = models.BooleanField(default=False, null=False, blank=False)
    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)


class Comment(MPTTModel):
    text = models.TextField(null=False, blank=False)
    author = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    related_to = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    #
    # class MPTTMeta:
    #     order_insertion_by = likeCounter #TODO