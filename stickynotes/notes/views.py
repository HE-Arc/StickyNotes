from django.shortcuts import render
from notes.models import StickyNote
from notes.forms import StickyNoteForm

# Create your views here.
def NotesPage(request):
    stickynotes = StickyNote.objects.all()

    form = StickyNoteForm(request.POST or None)

    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.user_created = request.user
        save_it.save()

    return render(request, 'notes/note.html', {'stickynotes' : stickynotes, 'form' : form})
