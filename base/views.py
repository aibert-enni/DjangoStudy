from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room, Topic, Message
from .forms import RoomForm
# Create your views here.



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None  else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(description__icontains=q))

    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)

def loginUser(request):
    page = "login"

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password doesn't correct")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def registerUser(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Username or password doesn't correct")

    context = {'form': form}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all().order_by('-created')
    participiants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(user=request.user, room=room, body=request.POST.get("comment-body"))
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, "messages": messages, 'participiants': participiants}

    return render(request, 'base/room.html', context)

@login_required(login_url="/login_page")
def createRoom(request):
    context = {'form': RoomForm()}

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/room_form.html', context)

@login_required(login_url="/login_page")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host and request.user.is_superuser == False:
        return HttpResponse("You haven't permission!")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.has_changed():
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            print("Nothing changed")

    context = {'form': form}

    return render(request, 'base/room_form.html', context)

@login_required(login_url="/login_page")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host and request.user.is_superuser == False:
        return HttpResponse("You haven't permission!")

    if request.method == "POST":
        room.delete()
        return redirect('home')

    context = {'obj': room}

    return render(request, 'base/delete.html', context)