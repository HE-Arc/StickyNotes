from django.conf.urls import url
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views
from accounts import views as accounts_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^notes', views.notes, name='view_notes'),

    path('chalkboard/<int:id_chalkboard>/manage/permissions/users/<int:id_user>/update', views.update_user_permissions, name='update_user_permissions'),
    path('chalkboard/<int:id_chalkboard>/manage/permissions/users/<int:id_user>/permissions', views.manage_user_permissions, name='manage_user_permissions'),
    path('chalkboard/<int:id_chalkboard>/manage/permissions/users/remove/user/<int:id_user>', views.remove_user_chalkboard, name='remove_user_chalkboard'),
    path('chalkboard/<int:id_chalkboard>/manage/permissions/users', views.manage_chalkboard_user_permission, name='permission_chalkboard'),

    # NOTES CRUD
    path('chalkboard/<int:id_chalkboard>/notes/create/<str:type_stickynote>', views.create_stickynotes, name='create_stickynotes'),
    path('chalkboard/<int:id_chalkboard>/notes/delete/<int:id_stickynote>', views.delete_stickynotes, name='delete_stickynotes'),
    path('chalkboard/<int:id_chalkboard>/notes/update/<int:id_stickynote>', views.update_stickynotes, name='update_stickynotes'),

    #CHALKBOARD CRUD
    re_path(r'^chalkboard/(?P<pk>\d+)/delete', views.ChalkboardDeleteView.as_view(), name='delete_chalkboard'),
    re_path(r'^chalkboard/(?P<pk>\d+)/update', views.ChalkboardUpdateView.as_view(), name='update_chalkboard'),
    re_path(r'^chalkboard/create', views.ChalkboardCreateView.as_view(), name='create_chalkboard'),
    path('chalkboard/join/<int:id_chalkboard>', views.join_chalkboard, name='join_chalkboard'),
    path('chalkboard/leave/<int:id_chalkboard>', views.leave_chalkboard, name='leave_chalkboard'),
    re_path(r'^chalkboard/(?P<pk>\d+)', views.ChalkboardDetailView.as_view(), name='details_chalkboard'),
    re_path(r'^chalkboard/owns', views.OwnChalkboardListView.as_view(), name='own_chalkboard'),
    re_path(r'^chalkboard/joined', views.JoinedChalkboardListView.as_view(), name='joined_chalkboard'),
    re_path(r'^chalkboard/public', views.PublicChalkboardListView.as_view(), name='public_chalkboard'),

    # TODO: notes has to be replaced by something like this ..
    # url(r'^chalkboards/(?P<pk>\d+)/$', views.notes, name='notes'),
    # ACCOUNTS
    # url(r'^(?P<username>[\w.@+-]+)/$', views.user_profile, name='user_profile'),
    url(r'^register/$', accounts_views.register, name='register'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    # passwords
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
]
