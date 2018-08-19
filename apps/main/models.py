from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
from datetime import date
import re

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1 or len(postData['last_name']) < 1 or len(postData['email']) < 1 or len(postData['password']) < 1 or len(postData['password_confirm']) < 1:
            errors['missing_field'] = "All fields are required"
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['name'] = "Name must contain at least 2 characters"
        if postData['first_name'].isalpha() == False or postData['last_name'].isalpha() == False:
            errors['alphabetical_name'] = "Name must include alphabetical characters only"
        try:
            validate_email(postData['email'])
        except:
            errors['invalid_email'] = "Invalid email address!"
        if User.objects.filter(email=postData['email']):
            errors['duplicated_email'] = "This email already exists!"
        if len(postData['password']) < 8:
            errors['password_length'] = "Password must contain at least 8 characters"
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Passwords don't match"
        # if not re.findall('\d', postData['password']):
        #     errors['missing_digit'] = "Password must contain at least 1 number"
        # if not re.findall('\w', postData['password']):
        #     errors['missing_letter'] = "Password must contain at least 1 alphabetical character"
        # if not re.findall('[()[\]{}|\\`~!@#$%^&amp;*_\-+=;:\'",<>./?]', postData['password']):
        #     errors['missing_special_chars'] = "Password must contain at least 1 special character"
        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        start_date = postData['travel_start_date']
        end_date = postData['travel_end_date']
        today = str(date.today())
        if len(postData['destination']) < 1 or len(postData['desc']) < 1 or len(postData['travel_start_date']) < 1 or len(postData['travel_end_date']) < 1:
            errors['missing_destination'] = "All fields are required!"
        if start_date < today or start_date > end_date:
            errors['wrong_start_date'] = "Something's wrong with the order of your travel dates!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    travel_start_date = models.DateField()
    travel_end_date = models.DateField()
    description = models.TextField()
    planner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='planned_trips')
    travelers = models.ManyToManyField(User, related_name='joined_trips')
    objects = TripManager()
    

