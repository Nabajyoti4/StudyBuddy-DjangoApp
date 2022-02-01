from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render

rooms = [
    {'id' : 1, 'name' : 'Lets Learn python'},
    {'id' : 2, 'name' : 'Desing with me'},
    {'id' : 3, 'name' : 'Frontend developers'}
]

# Create your views here.
def home(request):
    context = {'rooms' : rooms}
    return render(request, 'base/home.html', context)

def room(request):
    return render(request, 'base/room.html')