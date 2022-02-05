from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm


# Create your views here.
def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
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

    context = {'page' : page}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')

def register_user(request):
    page = 'register'
    form = UserCreationForm()
    context = {
        'form' : form,
        'page' : page
    }

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # return user object instead of saving it
            user.username = user.username.lower()
            user.save()
            # login user after saving it
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('register')

    return render(request, 'base/login_register.html',context)

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
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms' : rooms,
     'topics' : topics,
     'room_messages' : room_messages,
     'rooms_count' : rooms_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    # Get room by id
    room = Room.objects.get(pk=pk)
    room_messages = Message.objects.all()
    participants = room.participants.all()
    context = {
        'room' : room,
        'room_messages' : room_messages,
        'participants' : participants
        }
    return render(request, 'base/room.html', context)

@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            user=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def update_room(request, pk):
    room = Room.objects.get(pk=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user  != room.user:
        return HttpResponse('You are not allowed to edit this room')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room' : room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def delete_room(request, pk):
    room = Room.objects.get(pk=pk)

    if request.user  != room.user:
        return HttpResponse('You are not allowed to delete this room')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)

@login_required(login_url='/login')
def create_comment(request):
    if request.method == 'POST':
        room_id = request.POST.get('room')
        print(room_id)
        room = Room.objects.get(pk=room_id)
        room.participants.add(request.user)
        user = request.user
        message = request.POST.get('body')
        Message.objects.create(room=room, user=user, body=message)
        return redirect('room', pk=room_id)
    return HttpResponse('Not allowed')

@login_required(login_url='/login')
def delete_comment(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this message')

    room = message.room
    message.delete()
    return redirect('room', pk=room.pk)


# User views
def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user' : user,
        'rooms' : rooms,
        'room_messages' : room_messages,
        'topics' : topics
        }
    return render(request, 'base/profile.html', context)

@login_required(login_url='/login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            return redirect('user_profile', pk=user.id)

    context = {'form':form}
    return render(request, 'base/update_user.html', context)
