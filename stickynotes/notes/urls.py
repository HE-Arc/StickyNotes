from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^notes/$', views.NotesPage, name='notes'),
]
