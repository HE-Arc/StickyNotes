from django.contrib import admin
from .models import StickyNote, ImageStickyNote, VideoStickyNote, Chalkboard

# Register your models here.
class StickyNoteAdmin(admin.ModelAdmin):
    class Meta:
        model = StickyNote

class ImageStickyNoteAdmin(admin.ModelAdmin):
    class Meta:
        model = ImageStickyNote

class VideoStickyNoteAdmin(admin.ModelAdmin):
    class Meta:
        model = VideoStickyNote

admin.site.register(StickyNote, StickyNoteAdmin)
admin.site.register(ImageStickyNote, ImageStickyNoteAdmin)
admin.site.register(VideoStickyNote, VideoStickyNoteAdmin)
admin.site.register(Chalkboard)
