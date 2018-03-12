from django.conf.urls import url
from django.urls import path

from . import views
from accounts import views as accounts_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^notes', views.notes, name='view_notes'),
    # ACCOUNTS
    url(r'^register/$', accounts_views.register, name='register'),
    # url(r'^register/$', accounts_views.Register.as_view(), name='register'),
    # NOTES CRUD
    path('create/<str:type_stickynote>', views.create, name='create_stickynotes'),
    path('delete/<int:id_stickynote>', views.delete, name='delete_stickynotes'),
    path('update/<int:id_stickynote>', views.update, name='update_stickynotes'),
]
