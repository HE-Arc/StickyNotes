from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home),
    path('create', views.create, name='create_stickynotes'),
    path('delete/<int:id_stickynote>', views.delete, name='delete_stickynotes'),
    path('update/<int:id_stickynote>', views.update, name='update_stickynotes'),
]
