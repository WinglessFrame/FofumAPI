from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    text = models.TextField(null=False, blank=False)
    is_published = models.BooleanField(default=False, null=False, blank=False)
    creator = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
