from django import forms
from notes.models import StickyNote

class StickyNoteForm(forms.ModelForm):
    class Meta:
        model = StickyNote
        # fields = '__all__'
        exclude = ('user_created',) # __all__
