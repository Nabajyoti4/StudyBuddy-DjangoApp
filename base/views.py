from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render
from .models import Room



# Create your views here.
def home(request):
    rooms = Room.objects.all()
    context = {'rooms' : rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    # Get room by id
    room = Room.objects.get(pk=pk)
    context = {'room' : room}
    return render(request, 'base/room.html', context)