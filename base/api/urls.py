from django.urls import path
from . import views

urlpatterns = [
    path('rooms', views.get_rooms, name='get_rooms'),
    path('rooms/<str:id>', views.get_room, name='get_room'),
]


