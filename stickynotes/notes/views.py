from django.shortcuts import render
from django.shortcuts import redirect
from notes.models import StickyNote
from notes.forms import StickyNoteForm

# Create your views here.
def home(request):
    stickynotes = StickyNote.objects.all()
    return render(request, 'notes/note.html', {'stickynotes' : stickynotes})

def create(request):
    stickynotes = StickyNote.objects.all()
    form = StickyNoteForm(request.POST or None)
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.user_created = request.user
        save_it.save()
        return redirect(home)
    return render(request, 'notes/note_create_form.html', {'stickynotes' : stickynotes, 'form' : form})

def delete(request, id_stickynote):
    stickynote = StickyNote.objects.get(id=id_stickynote)
    stickynote.delete()
    return redirect(home)
