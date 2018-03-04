from django.contrib import admin
from .models import StickyNote, Chalkboard, StickyNoteType

# Register your models here.
class StickyNoteAdmin(admin.ModelAdmin):
    class Meta:
        model = StickyNote

admin.site.register(StickyNote, StickyNoteAdmin)
admin.site.register(Chalkboard)
admin.site.register(StickyNoteType)
