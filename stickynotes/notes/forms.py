from django import forms
from notes.models import StickyNote, ImageStickyNote, VideoStickyNote

class StickyNoteForm(forms.ModelForm):
    class Meta:
        model = StickyNote
        # fields = '__all__'
        exclude = ('user_created',) # __all__

class ImageStickyNoteForm(forms.ModelForm):
    class Meta:
        model = ImageStickyNote
        exclude = ('user_created', 'text_content')

class VideoStickyNoteForm(forms.ModelForm):
    class Meta:
        model = VideoStickyNote
        exclude = ('user_created', 'text_content')
