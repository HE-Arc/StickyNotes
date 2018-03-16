"""
    links:
        - https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-user-id-in-django
        - https://stackoverflow.com/questions/14026750/django-model-filtering-by-user-always
"""
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from notes.models import *
from notes.forms import StickyNoteForm, ImageStickyNoteForm, VideoStickyNoteForm, ChalkboardForm

# Create your views here.
# Global ??
type_stickynotes = [StickyNote, ImageStickyNote, VideoStickyNote]

def home(request):
    return render(request, 'home.html')

@login_required
def chalkboards(request):
    chlks = Chalkboard.objects.filter(user_created=request.user)
    return render(request, 'chalkboards/list_chalkboard.html', {'chlks' : chlks})

@login_required
def display_chalkboards(request, id_chalkboard):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard, user_created=request.user)
    stickynotes = StickyNote.objects.filter(chalkboard_id=chlk.id)
    return render(request, 'chalkboards/chalkboard.html', {'chlk' : chlk, 'stickynotes' : stickynotes, 'type_stickynotes' : type_stickynotes})

@login_required
def notes(request): # TODO: has to be changed somehow to allow passing from CHLK to NOTES
    stickynotes = StickyNote.objects.filter()
    return render(request, 'notes/note.html', {'stickynotes' : stickynotes, 'type_stickynotes' : type_stickynotes})

@login_required
def create_stickynotes(request, type_stickynote, id_chalkboard):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
    #try:
#        groupChalkboard = GroupChalkboard.objects.get(chalkboard=chlk, user_created=request.user)
#    except:
#        raise PermissionDenied
    form = None
    if type_stickynote == "image":
        form = ImageStickyNoteForm(request.POST or None)
    elif type_stickynote == "video":
        form = VideoStickyNoteForm(request.POST or None)
    elif type_stickynote == "text":
        form = StickyNoteForm(request.POST or None)
    if form is None:
        raise Http404
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.user_created = request.user
        save_it.chalkboard = chlk
        save_it.save()
        return redirect(display_chalkboards, id_chalkboard)
    return render(request, 'notes/note_create_form.html', {'type_stickynote' : type_stickynote, 'form' : form})

@login_required
def update_stickynotes(request, id_stickynote):
    stickynote = get_object_or_404(StickyNote, id=id_stickynote, user_created=request.user)
    form = StickyNoteForm(request.POST or None, instance=stickynote)
    if form.is_valid():
        form.save()
        return redirect(notes)
    return render(request, "notes/note_create_form.html", {'form': form})

@login_required
def delete_stickynotes(request, id_stickynote):
    stickynote = get_object_or_404(StickyNote, id=id_stickynote, user_created=request.user)
    stickynote.delete()
    return redirect(notes)

@login_required
def create_chalkboard(request):
    form = ChalkboardForm(request.POST or None)
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.user_created = request.user
        save_it.save()
        # Create auto group, creator is the admin
        group_permission = GroupPermissionChalkboard(user_id=request.user, )
        #groupChalkboard = GroupChalkboard(chalkboard=save_it, user_created=request.user, is_admin=True)
        #groupChalkboard.save()
        return redirect(chalkboards)
    return render(request, 'chalkboards/chalkboard_create_form.html', {'form' : form})
