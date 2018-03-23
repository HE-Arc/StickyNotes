from django import forms
from notes.models import StickyNote, ImageStickyNote, VideoStickyNote, Chalkboard

class StickyNoteForm(forms.ModelForm):
    class Meta:
        model = StickyNote
        fields = ('title', 'text_content', 'is_hidden')

class ImageStickyNoteForm(forms.ModelForm):
    class Meta:
        model = ImageStickyNote
        fields = ('title', 'image_content', 'is_hidden')

class VideoStickyNoteForm(forms.ModelForm):
    class Meta:
        model = VideoStickyNote
        fields = ('title', 'video_content', 'is_hidden')

class ChalkboardForm(forms.ModelForm):
    class Meta:
        model = Chalkboard
        exclude = ('user_created', 'group_permission')

class PermissionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        checkboxs = kwargs.pop('checkboxs')
        super(PermissionForm, self).__init__(*args, **kwargs)

        for i, key in enumerate(checkboxs.keys()):
            value = checkboxs[key]
            self.fields[key] = forms.BooleanField(required=False, initial=value)

    def save(self):
        return self.cleaned_data
