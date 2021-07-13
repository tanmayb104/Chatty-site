from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateRoomForm
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from accounts.models import CustomUser
from django.contrib import messages
from django.db.models import Q

# Create your views here.

@login_required
def createroom(request):
    form = CreateRoomForm()
    if request.method == 'POST':
        form = CreateRoomForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            instance.participants.add(request.user)
            instance.save()
            messages.success(request, "You successfully created a new room")
            return redirect('rooms')

    return render(request, 'rooms/createroom.html', {'form': form})


@login_required
def rooms(request):

    data = {}
    rooms = Room.objects.filter(participants__in=[request.user])
    user = get_object_or_404(CustomUser, id=request.user.id)
    data["rooms"] = rooms
    data["user"] = user
    return render(request, 'rooms/rooms2.html', data)


@login_required
def joinroom(request):

    if request.method == 'POST':
        code = request.POST["code"]
        room = get_object_or_404(Room, code=code)
        room.participants.add(request.user)
        messages.success(request, f"You have successfully joined the room {room.name}")
        return redirect('rooms')
    return render(request, 'rooms/joinroom.html')


@login_required
def detailroom(request, code):

    data = {}
    rooms = Room.objects.filter(participants__in=[request.user])
    user = get_object_or_404(CustomUser, id=request.user.id)
    data["rooms"] = rooms
    data["user"] = user
    data["code"] = code
    room = get_object_or_404(Room, code=code)
    data["room"] = room
    return render(request, 'rooms/detailroom.html', data)



@login_required
def searchroom(request):

    pk = request.GET['search']
    rooms = Room.objects.filter(Q(name__icontains=pk))
    return render(request, 'rooms/searchroom2.html', {'rooms': rooms}) 


@login_required
def settings(request):

    data = {}
    user = get_object_or_404(CustomUser, id=request.user.id)
    data["user"] = user
    return render(request, 'rooms/settings.html', data) 


@login_required
def joinmeeting(request, code): 

    data = {}
    user = get_object_or_404(CustomUser, id=request.user.id)
    data["user"] = user
    data["code"] = code
    return render(request, 'rooms/meeting.html', data)
