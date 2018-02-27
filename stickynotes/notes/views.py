from django.shortcuts import render
from notes.models import StickyNote

# Create your views here.
def home(request):
    stickynotes = StickyNote.objects.all()
    return render(request, 'notes/note.html', {'stickynotes' : stickynotes})
