"""
    links:
        - https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-user-id-in-django
        - https://stackoverflow.com/questions/14026750/django-model-filtering-by-user-always
"""
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import get_user_model

from notes.models import StickyNote, ImageStickyNote, VideoStickyNote, Chalkboard, JoinChalkboard, StickyNoteType
from notes.forms import StickyNoteForm, ImageStickyNoteForm, VideoStickyNoteForm, ChalkboardForm, PermissionForm

from guardian.shortcuts import assign_perm, get_perms, get_perms_for_model, remove_perm, get_user_perms, get_objects_for_user
from guardian.core import ObjectPermissionChecker
from guardian.decorators import permission_required_or_403
from guardian.utils import clean_orphan_obj_perms
from guardian.models import UserObjectPermission
from guardian.forms import UserObjectPermissionsForm, BaseObjectPermissionsForm
from guardian.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse

from django_tables2 import RequestConfig
from .tables import UserJoinTable
from django_tables2.columns import Column

# Create your views here.
type_stickynotes = [StickyNoteType.TEXT, StickyNoteType.IMAGE, StickyNoteType.VIDEO]

def home(request):
    return render(request, 'home.html')

@login_required
def notes(request):
    stickynotes = StickyNote.objects.filter()
    return render(request, 'notes/note.html', {'stickynotes' : stickynotes, 'type_stickynotes' : type_stickynotes})

@login_required
@permission_required_or_403('notes.stickynote_create_own', (Chalkboard, 'id', 'id_chalkboard'))
def create_stickynotes(request, id_chalkboard, type_stickynote):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
    form = None
    if type_stickynote == StickyNoteType.IMAGE.label:
        form = ImageStickyNoteForm(request.POST or None)
    elif type_stickynote == StickyNoteType.VIDEO.label:
        form = VideoStickyNoteForm(request.POST or None)
    elif type_stickynote == StickyNoteType.TEXT.label:
        form = StickyNoteForm(request.POST or None)
    if form is None:
        raise Http404
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.user_created = request.user
        save_it.chalkboard = chlk
        save_it.type = type_stickynote
        save_it.save()
        return redirect('details_chalkboard', id_chalkboard)
    return render(request, 'notes/note_form.html', {'type_stickynote' : type_stickynote, 'form' : form})

@login_required
def update_stickynotes(request, id_chalkboard, id_stickynote):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
    checker = ObjectPermissionChecker(request.user)
    stickynote = get_object_or_404(StickyNote, id=id_stickynote)
    can_update = False
    if request.user == stickynote.user_created and checker.has_perm('stickynote_update_own', chlk):
        can_update = True
    elif checker.has_perm('stickynote_update_all', chlk):
        can_update = True
    if can_update:
        form = None
        if stickynote.type == StickyNoteType.IMAGE:
            image_stickynotes = get_object_or_404(ImageStickyNote, stickynote_ptr_id=stickynote.id)
            form = ImageStickyNoteForm(request.POST or None, instance=image_stickynotes)
        elif stickynote.type == StickyNoteType.VIDEO:
            video_stickynotes = get_object_or_404(VideoStickyNote, stickynote_ptr_id=stickynote.id)
            form = VideoStickyNoteForm(request.POST or None, instance=video_stickynotes)
        elif stickynote.type == StickyNoteType.TEXT:
            form = StickyNoteForm(request.POST or None, instance=stickynote)
        if form is None:
            raise Http404
        if form.is_valid():
            form.save()
            messages.success(request, 'Update succes')
            return redirect('details_chalkboard', id_chalkboard)
    else:
        messages.warning(request, 'You don\'t have permission')
        return redirect('details_chalkboard', id_chalkboard)
    return render(request, "notes/note_form.html", {'form': form})

@login_required
def delete_stickynotes(request, id_chalkboard, id_stickynote):
    checker = ObjectPermissionChecker(request.user)
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
    stickynote = get_object_or_404(StickyNote, id=id_stickynote)
    can_delete = False
    if request.user == stickynote.user_created and checker.has_perm('stickynote_delete_own', chlk):
        can_delete = True
    elif checker.has_perm('stickynote_delete_all', chlk):
        can_delete = True
    if can_delete:
        stickynote.delete()
        messages.success(request, 'Delete succes')
    else:
        messages.warning(request, 'You don\'t have permission')
    return redirect('details_chalkboard', id_chalkboard)

@login_required
def join_chalkboard(request, id_chalkboard):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
    try:
        user_join = JoinChalkboard.objects.get(chalkboard=chlk, user_id=request.user)
    except:
        user_join = None
    if chlk.is_private and not user_join:
        return redirect('own_chalkboard')
    if chlk.is_private:
        return redirect('details_chalkboard', id_chalkboard)
    # default permision (CRUD own notes)
    assign_default_permission_join_chalkboard(request.user, chlk)
    JoinChalkboard.objects.create(chalkboard=chlk, user=request.user)
    return redirect('details_chalkboard', id_chalkboard)

@login_required
def leave_chalkboard(request, id_chalkboard):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
    user_join = JoinChalkboard.objects.get(chalkboard=chlk, user_id=request.user)
    if user_join:
        user_join.delete()
    return redirect('own_chalkboard')


@login_required
def manage_chalkboard_user_permission(request, id_chalkboard):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
    if check_permissions(request.user, chlk, ['chalkboard_manage_permission_user']):
        user_joined_ids = JoinChalkboard.objects.filter(chalkboard=chlk).values_list('user_id', flat=True)
        users = get_user_model().objects.filter(id__in=user_joined_ids)
        for user in users:
            user.remove_column = [reverse('remove_user_chalkboard', kwargs={'id_chalkboard': chlk.id, 'id_user': user.id}), 'delete.png']
            user.perm_column = [reverse('manage_user_permissions', kwargs={'id_chalkboard': chlk.id, 'id_user': user.id}), 'manage']
        users_table = UserJoinTable(data=users)
        RequestConfig(request, paginate={'per_page': 10}).configure(users_table)
        return render(request, 'permissions/permission_chalkboard.html', {'users_table': users_table, 'chalkboard': chlk})
    return redirect('details_chalkboard', id_chalkboard)

@login_required
def manage_user_permissions(request, id_chalkboard, id_user):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
    if check_permissions(request.user, chlk, ['chalkboard_manage_permission_user']):
        user_join = get_object_or_404(JoinChalkboard, chalkboard=chlk, user_id=id_user)
        user = get_user_model().objects.get(id=id_user)
        permissions_rows = dict()
        permissions_user = dict()
        # get all permissions chalkboard
        for perm in get_perms_for_model(Chalkboard):
            permissions_rows[perm.codename] = perm.name
            permissions_user[perm.codename] = False # default false permission
        for perm in get_user_perms(user, chlk):
            permissions_user[perm] = True
        form = PermissionForm(request.POST or None, checkboxs=permissions_user)
        if form.is_valid():
            permissions_datas = form.save()

            for codename, value in permissions_datas.items():
                has_perm = check_permissions(user, chlk, [codename])
                if value:
                    if not has_perm:
                        assign_permission(codename, user, chlk)
                else:
                    if has_perm:
                        remove_perm(codename, user, chlk)
            messages.success(request, 'Permissions saved.')
        return render(request, 'permissions/permissions_user_chalkboard.html', {'user_id' : id_user, 'chalkboard': chlk, 'permissions_rows': permissions_rows, 'form': form})
    return redirect('permission_chalkboard', id_chalkboard)

@login_required
def remove_user_chalkboard(request, id_chalkboard, id_user):
    chlk = get_object_or_404(Chalkboard, id=id_chalkboard)
    if check_permissions(request.user, chlk, ['chalkboard_manage_permission_user']):
        user_join = get_object_or_404(JoinChalkboard, chalkboard=chlk, user_id=id_user)
        user_join.delete()
        messages.success(request, 'This user has been delete from the chalkboard.')
        return redirect('permission_chalkboard', id_chalkboard)
    return redirect('details_chalkboard', id_chalkboard)

def check_permissions(user, object, permissions):
    checker = ObjectPermissionChecker(user)
    perm = True
    for perm in permissions:
        if not checker.has_perm(perm, object):
            return False
    return perm


class OwnChalkboardListView(LoginRequiredMixin, ListView):

    model = Chalkboard
    template_name = 'chalkboards/chalkboards.html'

    def get_context_data(self, **kwargs):
        # Get context super-class
        context = super(OwnChalkboardListView, self).get_context_data(**kwargs)
        context['chalkboards'] = Chalkboard.objects.filter(user_created=self.request.user)
        context['joined_chalkboards_id'] = JoinChalkboard.objects.filter(user=self.request.user).values_list('chalkboard_id', flat=True)
        context['chalkboard_title'] = 'My chalkboards'
        context['chalkboard_empty_message'] = 'You don\'t have a chalkboard yet! \nGo ahead and create one!'
        return context

class JoinedChalkboardListView(LoginRequiredMixin, ListView):

    model = Chalkboard
    template_name = 'chalkboards/chalkboards.html'

    def get_context_data(self, **kwargs):
        # Get context super-class
        context = super(JoinedChalkboardListView, self).get_context_data(**kwargs)
        join_chlks_id = JoinChalkboard.objects.filter(user=self.request.user).values_list('chalkboard_id', flat=True)
        context['chalkboards'] = Chalkboard.objects.filter(id__in=join_chlks_id)
        context['joined_chalkboards_id'] = join_chlks_id
        context['chalkboard_title'] = 'Joined chalkboards'
        context['chalkboard_empty_message'] = 'You didn\'t join a chalkboard yet! Browse through the Public Chalkboards list to find some!'
        return context

class PublicChalkboardListView(LoginRequiredMixin, ListView):

    model = Chalkboard
    template_name = 'chalkboards/chalkboards.html'

    def get_context_data(self, **kwargs):
        # Get context super-class
        context = super(PublicChalkboardListView, self).get_context_data(**kwargs)
        context['chalkboards'] = Chalkboard.objects.exclude(user_created=self.request.user).filter(is_private=False, is_active=True)
        context['joined_chalkboards_id'] = JoinChalkboard.objects.filter(user=self.request.user).values_list('chalkboard_id', flat=True)
        context['chalkboard_title'] = 'Public chalkboards'
        context['chalkboard_empty_message'] = 'Hehe you\'re the first person here! Congrats! Go ahead and create a new Chalkboard!'
        return context

class ChalkboardDetailView(LoginRequiredMixin, DetailView):

    model = Chalkboard
    template_name = 'chalkboards/single_chalkboard.html'

    def get_object(self):
        # Get chalboard
        chlk = super(ChalkboardDetailView, self).get_object()
        chlk.save()
        return chlk

    def get_context_data(self, **kwargs):
        # Get context super-class
        context = super(ChalkboardDetailView, self).get_context_data(**kwargs)
        context['stickynotes'] = StickyNote.objects.filter(chalkboard_id=self.object, is_hidden=False)
        context['type_stickynotes'] = type_stickynotes
        return context

class ChalkboardCreateView(LoginRequiredMixin, CreateView):

    model = Chalkboard
    template_name = 'chalkboards/chalkboard_create_form.html'
    form_class = ChalkboardForm

    def get_success_url(self):
        return reverse('details_chalkboard', kwargs={'pk' : self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_created = self.request.user
        self.object.save()
        assign_permission('stickynote_create_own', self.request.user, self.object)
        assign_permission('stickynote_update_own', self.request.user, self.object)
        assign_permission('stickynote_delete_own', self.request.user, self.object)
        assign_permission('stickynote_read_all', self.request.user, self.object)
        assign_permission('stickynote_update_all', self.request.user, self.object)
        assign_permission('stickynote_delete_all', self.request.user, self.object)
        assign_permission('chalkboard_add_user', self.request.user, self.object)
        assign_permission('chalkboard_remove_user', self.request.user, self.object)
        assign_permission('chalkboard_manage_permission_user', self.request.user, self.object)
        assign_permission('chalkboard_manage_permission', self.request.user, self.object)
        assign_permission('chalkboard_update', self.request.user, self.object)
        assign_permission('chalkboard_delete', self.request.user, self.object)
        messages.success(self.request, 'Your chalkboard has been successfully created')
        return redirect(self.get_success_url())

class ChalkboardUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Chalkboard
    template_name = 'chalkboards/chalkboard_update_form.html'
    form_class = ChalkboardForm
    permission_required = 'notes.chalkboard_update'
    return_403 = True

    def get_success_url(self):
        return reverse('details_chalkboard', kwargs={'pk' : self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_created = self.request.user
        self.object.save()
        messages.success(self.request, 'Your chalkboard has been successfully modified')
        return redirect(self.get_success_url())

class ChalkboardDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Chalkboard
    template_name = 'chalkboards/chalkboard_delete_form.html'
    permission_required = 'notes.chalkboard_delete'
    return_403 = True

    def get_success_url(self):
        return reverse('own_chalkboard')

# Fonctions
def assign_permission(permission, user, object):
    assign_perm(permission, user, object)

def assign_default_permission_join_chalkboard(user, object):
    assign_permission('stickynote_create_own', user, object)
    assign_permission('stickynote_update_own', user, object)
    assign_permission('stickynote_delete_own', user, object)
