from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'gotGOT_app/index.html')

def reg(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        newUser = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        )
        newUser.save()
        user = User.objects.get(email = request.POST['email'])
        request.session['user'] = user.id
        request.session['first_name'] = user.first_name
        return redirect('/dashboard')

def log(request):
    errors = User.objects.userValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['user'] = user.id
        request.session['first_name'] = user.first_name
    return redirect('/dashboard')

def dashboard(request):
    if 'user' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user'])
    context = {}
    context['user'] = user
    context['event'] = Event.objects.all()
    context['hosted'] = len(user.hosts.all())
    context['joined'] = len(user.joiners.all())
    context['yourEvents'] = User.objects.get(id = user.id).joiners.all()
    return render(request, 'gotGOT_app/dashboard.html', context)

def shows(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {}
    context['event'] = Event.objects.all()
    return render(request, 'gotGOT_app/shows.html', context)

def newShow(request):
    if 'user' not in request.session:
        return redirect('/')
    return render(request, 'gotGOT_app/new-show.html')

def createShow(request):
    user = User.objects.get(id=request.session['user'])
    newEvent = Event.objects.create(
        title = request.POST['title'],
        genre = request.POST['genre'],
        time = request.POST['time'],
        location = request.POST['location'],
        hosts = user
    )
    newEvent.joiners.add(user)
    newEvent.save()
    return redirect('/shows')

def showDesc(request, showID):
    if 'user' not in request.session:
        return redirect('/')
    joiners = Event.objects.get(id = showID).joiners.all()
    context = {}
    context['show'] = Event.objects.get(id = showID)
    context['joiners'] = joiners
    return render(request, 'gotGOT_app/movies.html', context)

def joinEvent(request, showID):
    if 'user' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user'])
    event = Event.objects.get(id = showID)
    event.joiners.add(user)
    event.save()
    return redirect('/shows')

def delete(request, showID):
    deleteShow = Event.objects.get(id = showID)
    deleteShow.delete()
    return redirect('/shows')

def logout(request):
    request.session.clear()
    return redirect('/')