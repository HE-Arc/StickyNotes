from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^notes', views.notes, name='view_notes'),
    path('register', views.Register.as_view(), name='register'),
    path('create/<str:type_stickynote>', views.create, name='create_stickynotes'),
    path('delete/<int:id_stickynote>', views.delete, name='delete_stickynotes'),
    path('update/<int:id_stickynote>', views.update, name='update_stickynotes'),
]
