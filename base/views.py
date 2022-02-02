from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages
from .models import Room, Topic
from .forms import RoomForm


# Create your views here.
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Not found')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
        
    return render(request, 'base/login_register.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def home(request):
    # get the query params
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    # get the rooms that match the query
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()
    rooms_count = rooms.count()
    context = {'rooms' : rooms,
     'topics' : topics,
     'rooms_count' : rooms_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    # Get room by id
    room = Room.objects.get(pk=pk)
    context = {'room' : room}
    return render(request, 'base/room.html', context)

def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)
            return HttpResponse('Form is not valid')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def update_room(request, pk):
    room = Room.objects.get(pk=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)
            return HttpResponse('Form is not valid')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def delete_room(request, pk):
    room = Room.objects.get(pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)