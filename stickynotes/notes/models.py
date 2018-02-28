from django.db import models
from django.conf import settings

# Create your models here.
class StickyNoteType(models.Model):
    """Class represents a type of content for stickynote"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Group(models.Model):
    """Class reprensents a group of stickynote"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class StickyNote(models.Model):
    """Class represents a stickynote"""
    content = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(StickyNoteType, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
