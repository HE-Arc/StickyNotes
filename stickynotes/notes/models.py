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


# TODO
class FavoriteChalkboards(models.Model):
    """ Contains a users's favorite chalkboards """
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    favorites = models.ForeignKey(Chalkboard, on_delete=models.CASCADE)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )


class StickyNote(models.Model):
    """ Contains the data created by the users """
    title = models.CharField(max_length=50)
    text_content = models.CharField(max_length=500)

    chalkboard = models.ForeignKey(Chalkboard, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    def __str__(self):
        return "text"


class ImageStickyNote(StickyNote):
    """ Contains the data created by the users """
    image_content = models.URLField() # not work yet (change)

    def __str__(self):
        return "image"


class VideoStickyNote(StickyNote):
    """ Contains the data created by the users """
    video_content = EmbedVideoField() # embed video content

    def __str__(self):
        return "video"
