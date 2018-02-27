from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Group(models.Model):
    """Class represents a group"""
    name = models.CharField(max_length=50)

class StickyNote(models.Model):
    """Class represents a stickynote"""
    content = models.CharField(max_length=255)
    content_type = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_created = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
