from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from accounts import views as accounts_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^notes', views.notes, name='view_notes'),
    # ACCOUNTS
    url(r'^register/$', accounts_views.register, name='register'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
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
    # NOTES CRUD
    path('create/<str:type_stickynote>', views.create, name='create_stickynotes'),
    path('delete/<int:id_stickynote>', views.delete, name='delete_stickynotes'),
    path('update/<int:id_stickynote>', views.update, name='update_stickynotes'),
]
