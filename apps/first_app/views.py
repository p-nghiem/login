from django.shortcuts import render, HttpResponse, redirect # Added HttpResponse, redirect
from time import gmtime, strftime
from django.utils.crypto import get_random_string
from random import *
import sys, re
import os, binascii
import bcrypt, hashlib # bcrypt instead of md5
from models import *
from django.contrib import messages
from django.contrib.auth import get_user_model

rejectEmail = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.

def register(request):
    if request.method == "POST":
      firstname = request.POST['firstname']
      lastname = request.POST['lastname']
      email = request.POST['email']
      password = request.POST['password']
      confirmpassword = request.POST['confirmpassword']
    # validator

      User = get_user_model()
      errors = User.objects.Validator(request.POST)
      print errors
      if len(errors):
        for tag, error in errors.iteritems():
          messages.error(request, error, extra_tags=tag)
  #   else:
  #       Course.objects.create(name = request.POST['name'], description = request.POST['description'])

      else:  # passed validation, register user
        #password_hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        encrypted_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        User.objects.create(first_name=firstname, last_name=lastname, email=email, password=encrypted_password)
        # User.objects.Create_user(request.POST)
        print "Successful registration"
        request.session['firstname'] = firstname
        return redirect('/success')
    return redirect('/')

def login(request):
    if request.method == "POST":

        errors = {}
        print "in user login"
        email = request.POST['email']
        password = request.POST['password']
        
        User = get_user_model()
        emailexists = User.objects.filter(email=email)

        if not rejectEmail.match(email):                              # Error email format
            errors['email'] = "Email is not valid"
            return redirect('/')

        # Check if password match
        else:
            # encrypted_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            # password_from_db = User.objects.filter(email=email).first()
            password_from_db = User.objects.get(email=email).password

            if bcrypt.checkpw(password.encode(), password_from_db.encode()):
                # this means we have a successful login!
                user_id = User.objects.get(email=email).id
                return redirect('/success')
            else:
                # invalid password!
                errors['password'] = "Password is not valid"
                print "Invalid password"
                print ('User entered:', encrypted_password)
                print ('Password from db:', password_from_db.encode())
                return redirect('/')

    return redirect('/')


def success(request):
    firstname = request.session['firstname']
#  context = {'firstname': firstname}

#   all_items = Item.objects.all()

#   context = {
#       'firstname': firstname,
#       'all_items': all_items
#   }
    items = [
      {'item': 'iPhone9', 'added_by': 'Mark', 'item_id': 101},
      {'item': 'MountainBike', 'added_by': 'Jeffrey', 'item_id': 102},
      {'item': 'Macbook Pro', 'added_by': 'Sheila', 'item_id': 103},
      {'item': 'Hiking Bag', 'added_by': 'Steve', 'item_id': 104}
    ]
    otheruseritems = [
      {'item': 'Rolex Watch', 'added_by': 'John', 'item_id': 105},
      {'item': 'Hotel Stay', 'added_by': 'Stan', 'item_id': 106},
      {'item': 'BBQ Grill', 'added_by': 'Sofia', 'item_id': 107},
      {'item': 'Zumba DVD', 'added_by': 'Jeric', 'item_id': 108}
    ]

    context = {
      'all_items': items,
      'all_otheruseritems': otheruseritems
      }

    return render(request,'dashboard.html', context)


def create (request):
    pass # validate item and save in database
    return render(request,'create.html')

def add_new_item (request):
    pass # validate item and save in database
    return redirect ('/dashboard')

def add_to_wishlist (request):
    pass  
    return redirect ('/dashboard')

def remove_from_wishlist (request):
    pass  
    return redirect ('/dashboard')

def delete_from_database (request):
    pass # delete from the db
    return redirect ('/databoard')


# the index function is called when root is visited

def index(request):

  return render(request,'index.html')


