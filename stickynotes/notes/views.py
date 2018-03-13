"""
    links:
        - https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-user-id-in-django
        - https://stackoverflow.com/questions/14026750/django-model-filtering-by-user-always
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from notes.models import StickyNote, ImageStickyNote, VideoStickyNote, Chalkboard
from notes.forms import StickyNoteForm, ImageStickyNoteForm, VideoStickyNoteForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required
def chalkboards(request):
    chlks = Chalkboard.objects.all()
    return render(request, 'chalkboards/chalkboard.html', {'chlks' : chlks})

@login_required
def notes(request): # TODO: has to be changed somehow to allow passing from CHLK to NOTES
    stickynotes = StickyNote.objects.filter()
    type_stickynotes = [StickyNote, ImageStickyNote, VideoStickyNote]
    return render(request, 'notes/note.html', {'stickynotes' : stickynotes, 'type_stickynotes' : type_stickynotes})

def create(request, type_stickynote):
    form = StickyNoteForm(request.POST or None)
    if type_stickynote == "image":
        form = ImageStickyNoteForm(request.POST or None)
    elif type_stickynote == "video":
        form = VideoStickyNoteForm(request.POST or None)

    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.user_created = request.user
        save_it.save()
        return redirect(notes)
    return render(request, 'notes/note_create_form.html', {'type_stickynote' : type_stickynote, 'form' : form})

def update(request, id_stickynote):
    stickynote = get_object_or_404(StickyNote, id=id_stickynote)
    form = StickyNoteForm(request.POST or None, instance=stickynote)
    if form.is_valid():
        form.save()
        return redirect(notes)
    return render(request, "notes/note_create_form.html", {'form': form})

def delete(request, id_stickynote):
    stickynote = StickyNote.objects.get(id=id_stickynote)
    stickynote.delete()
    return redirect(notes)
