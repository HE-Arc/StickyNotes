"""
    links:
        - https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-user-id-in-django
        - https://stackoverflow.com/questions/14026750/django-model-filtering-by-user-always
"""
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from notes.models import StickyNote, ImageStickyNote, VideoStickyNote, Chalkboard, JoinChalkboard
from notes.forms import StickyNoteForm, ImageStickyNoteForm, VideoStickyNoteForm, ChalkboardForm

from guardian.shortcuts import assign_perm, get_perms, remove_perm, get_user_perms, get_objects_for_user
from guardian.core import ObjectPermissionChecker
from guardian.decorators import permission_required_or_403

# Create your views here.
# Global ??
type_stickynotes = [StickyNote, ImageStickyNote, VideoStickyNote]

def home(request):
    return render(request, 'home.html')

@login_required
def notes(request): # TODO: has to be changed somehow to allow passing from CHLK to NOTES
    stickynotes = StickyNote.objects.filter()
    return render(request, 'notes/note.html', {'stickynotes' : stickynotes, 'type_stickynotes' : type_stickynotes})

@login_required
@permission_required_or_403('notes.stickynote_create_own', (Chalkboard, 'id', 'id_chalkboard'))
def create_stickynotes(request, id_chalkboard, type_stickynote):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
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
        return redirect(display_chalkboard, id_chalkboard)
    return render(request, 'notes/note_create_form.html', {'type_stickynote' : type_stickynote, 'form' : form})

@login_required
def update_stickynotes(request, id_chalkboard, id_stickynote):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
    checker = ObjectPermissionChecker(request.user)
    stickynote = get_object_or_404(StickyNote, id=id_stickynote)
    can_update = False
    if request.user == stickynote.user_created and checker.has_perm('stickynote_update_own', chlk):
        can_update = True
    elif request.user != stickynote.user_created and checker.has_perm('stickynote_update_all', chlk):
        can_update = True
    elif request.user == stickynote.user_created and checker.has_perm('stickynote_update_all', chlk):
        can_update = True
    if can_update:
        form = StickyNoteForm(request.POST or None, instance=stickynote)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update succes')
            return redirect(display_chalkboard, id_chalkboard)
    else:
        messages.warning(request, 'You don\'t have permission')
        return redirect(display_chalkboard, id_chalkboard)
    return render(request, "notes/note_create_form.html", {'form': form})

@login_required
def delete_stickynotes(request, id_chalkboard, id_stickynote):
    checker = ObjectPermissionChecker(request.user)
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
    stickynote = get_object_or_404(StickyNote, id=id_stickynote)
    can_delete = False
    if request.user == stickynote.user_created and checker.has_perm('stickynote_update_own', chlk):
        can_delete = True
    elif request.user != stickynote.user_created and checker.has_perm('stickynote_update_all', chlk):
        can_delete = True
    elif request.user == stickynote.user_created and checker.has_perm('stickynote_update_all', chlk):
        can_delete = True
    if can_delete:
        stickynote.delete()
        messages.success(request, 'Delete succes')
    else:
        messages.warning(request, 'You don\'t have permission')
    return redirect(display_chalkboard, id_chalkboard)

@login_required
def chalkboards(request):
    own_chlks = Chalkboard.objects.filter(user_created=request.user)
    join_chlks_id = JoinChalkboard.objects.filter(user_created=request.user).values('chalkboard_id')
    join_chlks = Chalkboard.objects.filter(id__in=join_chlks_id)
    public_chlks = Chalkboard.objects.exclude(user_created=request.user).filter(is_private=False, is_active=True)
    return render(request, 'chalkboards/chalkboards.html', {'own_chlks' : own_chlks, 'join_chlks' : join_chlks, 'public_chlks' : public_chlks})

@login_required
def display_chalkboard(request, id_chalkboard):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
    checker = ObjectPermissionChecker(request.user)
    stickynotes = StickyNote.objects.filter(chalkboard_id=chlk.id)
    return render(request, 'chalkboards/single_chalkboard.html', {'chlk' : chlk, 'stickynotes' : stickynotes, 'type_stickynotes' : type_stickynotes })

@login_required
def create_chalkboard(request):
    form = ChalkboardForm(request.POST or None)
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.user_created = request.user
        save_it.save()
        # creator has all the privileges
        assign_permission('stickynote_create_own', request.user, save_it)
        assign_permission('stickynote_update_own', request.user, save_it)
        assign_permission('stickynote_delete_own', request.user, save_it)
        assign_permission('stickynote_read_all', request.user, save_it)
        assign_permission('stickynote_update_all', request.user, save_it)
        assign_permission('stickynote_delete_all', request.user, save_it)
        assign_permission('chalkboard_add_user', request.user, save_it)
        assign_permission('chalkboard_remove_user', request.user, save_it)
        assign_permission('chalkboard_manage_permission_user', request.user, save_it)
        assign_permission('chalkboard_manage_permission', request.user, save_it)
        assign_permission('chalkboard_delete', request.user, save_it)
        messages.success(request, 'Your chalkboard has been successfully created')
        return redirect(chalkboards)
    return render(request, 'chalkboards/chalkboard_create_form.html', {'form' : form})

@login_required
@permission_required_or_403('notes.chalkboard_delete', (Chalkboard, 'id', 'id_chalkboard'))
def delete_chalkboard(request, id_chalkboard):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
    chlk.delete()
    return redirect(chalkboards)

@login_required
def join_chalkboard(request, id_chalkboard):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)

    # TODO check if chalkboard not private

    # default permision (CRUD own notes)
    assign_default_permission_join_chalkboard(request.user, chlk)
    JoinChalkboard.objects.create(chalkboard=chlk, user_created=request.user)
    return redirect(display_chalkboard, id_chalkboard)

@login_required
def leave_chalkboard(request, id_chalkboard):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
    for perm in get_user_perms(request.user, chlk):
        remove_perm(perm, request.user, chlk)
    JoinChalkboard.objects.filter(chalkboard=chlk, user_created=request.user).delete()
    return redirect(chalkboards)



# Fonctions
def assign_permission(permission, user, object):
    assign_perm(permission, user, object)

def assign_default_permission_join_chalkboard(user, object):
    assign_permission('stickynote_create_own', user, object)
    assign_permission('stickynote_update_own', user, object)
    assign_permission('stickynote_delete_own', user, object)
