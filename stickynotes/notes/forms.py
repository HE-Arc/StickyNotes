from django import forms
from notes.models import StickyNote, ImageStickyNote, VideoStickyNote, Chalkboard

class StickyNoteForm(forms.ModelForm):
    class Meta:
        model = StickyNote
        # fields = '__all__'
        exclude = ('user_created', 'chalkboard')

class ImageStickyNoteForm(forms.ModelForm):
    class Meta:
        model = ImageStickyNote
        exclude = ('user_created', 'text_content', 'chalkboard')

class VideoStickyNoteForm(forms.ModelForm):
    class Meta:
        model = VideoStickyNote
        exclude = ('user_created', 'text_content', 'chalkboard')

class ChalkboardForm(forms.ModelForm):
    class Meta:
        model = Chalkboard
        exclude = ('user_created', 'group_permission')
