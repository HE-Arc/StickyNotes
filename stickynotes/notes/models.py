"""
    Used links:
    - https://pypi.python.org/pypi/django-enumfields
    - http://django-embed-video.readthedocs.io/en/v1.1.0/index.html
"""

from django.db import models
from django.conf import settings

from enumfields import EnumField, Enum
from embed_video.fields import EmbedVideoField
# Create your models here.

class Type(Enum):
    """ Content types enumeration: Text, Image, Video (youtube, vimeo, (and soundcloud as well)) """
    TEXT = 't'
    IMAGE = 'i'
    VIDEO = 'v'

    class Labels:
        TEXT = 'Text'
        IMAGE = 'Image'
        VIDEO = 'Video'

class StickyNoteType(models.Model):
    """ Content types (using Type enum) """
    name = models.CharField(max_length=50)
    # name = EnumField(Type, max_length=1)  # doesn't work yet

    def __str__(self):
        return self.name

class Chalkboard(models.Model):
    """ Chalkboard containing different types of notes """
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name

class StickyNote(models.Model):
    """ Contains the data created by the users """
    title = models.CharField(max_length=50)
    # content = models.CharField(max_length=1000)   # text content
    content = EmbedVideoField() # embed video content

    chalkboard = models.ForeignKey(Chalkboard, on_delete=models.CASCADE)

    content_type = models.ForeignKey(StickyNoteType, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
