from django.contrib import admin
from .models import StickyNote

# Register your models here.
class StickyNoteAdmin(admin.ModelAdmin):
    class Meta:
        model = StickyNote

admin.site.register(StickyNote, StickyNoteAdmin)
