from django.shortcuts import render, redirect, HttpResponse
from django.utils import timezone
from django.contrib import messages
import bcrypt
from datetime import date
from .models import *

def index(request):
    if 'user' not in request.session:
        request.session['user'] = ""
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
        print("This is the user's first name", user.first_name)
        return redirect('travels')

def login(request):
    try: 
        user = User.objects.get(email=request.POST['email'])
    except User.DoesNotExist:
        messages.error(request, "Email address does not exists")
        return redirect('index')
    if bcrypt.checkpw(request.POST['password'].encode('utf8'), user.password.encode('utf8')) == False:
        messages.error(request, "Invalid password")
        return redirect('index')
    else:
        request.session['user'] = user.id
        return redirect('travels')

def logout(request):
    request.session.clear()
    return redirect('index')

def travels(request):
    try:
        user = User.objects.get(id=request.session['user'])    
    except:
        return redirect('index')
    travels = {
        'user': user,
        'planned_trips': Trip.objects.filter(planner=user),
        'my_trips': user.joined_trips.all(),
        'other_trips': Trip.objects.exclude(planner=user)
    }
    return render(request, 'main/travels.html', travels)

def cancel_as_planner(request, id):
    trip = Trip.objects.get(id=id)
    trip.planner = None
    trip.save()
    return redirect('travels')

def cancel_as_traveler(request, id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(id=request.session['user'])
    trip.travelers.remove(user)
    return redirect('travels')

def delete(request, id):
    Trip.objects.get(id=id).delete()
    return redirect('travels')

def view(request, id):
    user = User.objects.get(id=request.session['user'])    
    viewed_trip = Trip.objects.get(id=id)
    trip_planner = viewed_trip.planner
    other_users = viewed_trip.travelers.all()
    return render(request, 'main/view.html', {'user': user, 'viewed_trip': viewed_trip, 'trip_planner': trip_planner, 'other_users': other_users})

def join(request, id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(id=request.session['user'])
    trip.travelers.add(user)
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
        Trip.objects.create(destination=request.POST['destination'], travel_start_date=request.POST['travel_start_date'], travel_end_date=request.POST['travel_end_date'], description=request.POST['desc'], planner=user)
        return redirect('travels')

def go_back(request):
    return redirect('travels')

