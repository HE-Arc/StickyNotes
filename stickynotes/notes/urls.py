from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('create', views.create, name='create_stickynotes'),
    path('delete/<int:id_stickynote>', views.delete, name='delete_stickynotes')
]
