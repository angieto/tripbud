from django.shortcuts import render, redirect, HttpResponse
from django.utils import timezone
from django.contrib import messages
import bcrypt
from datetime import date
from .models import *

def index(request):
    return render(request, 'main/index.html')

def create(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('index')
    else:
        user_password = bcrypt.hashpw(request.POST['password'].encode('utf8'), bcrypt.gensalt(10))
        user_password = user_password.decode('utf8')
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=user_password)
        request.session['user'] = user.id
        return redirect('travels')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('index') 
    else:   
        user = User.objects.get(email=request.POST['email'])
        request.session['user'] = user.id
        return redirect('travels')

def logout(request):
    request.session.clear()
    return redirect('index')

def travels(request):
    user = User.objects.get(id=request.session['user'])    
    travels = {
        'user': user,
        'my_trips': user.joined_trips.all(),
        'other_trips': Trip.objects.exclude(travelers=user)
    }
    return render(request, 'main/travels.html', travels)

def delete(request, id):
    Trip.objects.get(id=id).delete()
    return redirect('travels')

def view(request, id):
    trip = Trip.objects.get(id=id)
    context = {
        'trip': trip,
        'users': User.objects.filter(joined_trips=trip).exclude(planned_trips=trip)
    }
    return render(request, 'main/view.html', context)

def join(request, id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(id=request.session['user'])
    trip.travelers.add(user)
    trip.save()
    return redirect('travels')

def cancel(request, id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(id=request.session['user'])
    trip.travelers.remove(user)
    trip.save()
    return redirect('travels')

def add_trip(request):
    return render(request, 'main/add_trip.html')

def add(request):
    errors = Trip.objects.trip_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('add_trip')
    else:
        user = User.objects.get(id=request.session['user'])
        trip = Trip.objects.create(
            destination=request.POST['destination'], 
            travel_start_date=request.POST['travel_start_date'], 
            travel_end_date=request.POST['travel_end_date'], 
            description=request.POST['desc'], 
            planner=user
        )
        trip.travelers.add(user) #add the user into the travelers table 
        trip.save()
        return redirect('travels')

def go_back(request):
    return redirect('travels')

