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
            encrypted_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            password_from_db=User.objects.filter(email=email).first()
            if bcrypt.checkpw(password_from_db.password.encode(), encrypted_password.encode()):
                # this means we have a successful login!
                print "Success"
                return redirect('/success')
            else:
                # invalid password!
                errors['password'] = "Password is not valid"
                print "Invalid password"
                print ('User entered:', encrypted_password)
                print ('Password from db:', password_from_db.password.encode())
                return redirect('/')

    return redirect('/')


def success(request):
  firstname = request.session['firstname']
  context = {'firstname': firstname}
  return render(request,'success.html', context)


# the index function is called when root is visited

def index(request):

  '''
  if 'gold_total' not in request.session:
    request.session['gold_total'] = 0  
    gold_total = 0
    print 'Gold Total'
    print gold_total
  if 'activity_log' not in request.session:
    request.session['activity_log'] = {}
  
  activity_log = request.session['activity_log']
  context = {'all_activities': activity_log}
  return render(request,'index.html', context)
  '''
  return render(request,'index.html')


###
# login registration from flask
###
'''

@app.route('/users/create', methods=['POST'])
def create_user():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    submit = request.form['submit']

    if request.method == "POST":
        if len(firstname) < 2:
            # Error first name
            print "Error in first name"
            flash("First name must be at least 2 characters long")
            return redirect('/')
        if len(lastname) < 2:
            # Error last name
            flash("Last name must be at least 2 characters long")
            return redirect('/')
        if not rejectEmail.match(email):
            flash("Email is not valid!")  # Error email
            return redirect('/')
        if len(password) < 8:
            # Error password
            flash("Password must be at least 8 characters long")
            return redirect('/')
        else:  
            flash(" {} successfully registered!".format(request.form['email']))
            salt =  binascii.b2a_hex(os.urandom(15))
            hashed_pw = md5.new(password + salt).hexdigest()
            insert_query = "INSERT INTO friends (first_name, last_name, email, password, salt, created_at, updated_at) VALUES (:firstname, :lastname, :email, :hashed_pw, :salt, NOW(), NOW())"
            query_data = { 'firstname': firstname, 'lastname': lastname, 'email': email, 'hashed_pw': hashed_pw, 'salt': salt}
            mysql.query_db(insert_query, query_data)
            return redirect('/success')
    return render_template('index.html')

@app.route('/users/login', methods=['POST'])
def login_user():

    if request.method == "POST":
        print "in user login"
        email = request.form['email']
        password = request.form['password']
        user_query = "SELECT * FROM friends WHERE friends.email = :email LIMIT 1"
        query_data = {'email': email}
        user = mysql.query_db(user_query, query_data)
        if len(user) != 0:
            encrypted_password = md5.new(password + user[0]['salt']).hexdigest()
            if user[0]['password'] == encrypted_password:
                # this means we have a successful login!
                flash("Successful login")
                return redirect('/success')
            else:
                # invalid password!
                flash("Invalid password")
                redirect('/')
        else:
            # invalid email!
            flash("Invalid email")
            redirect('/')
    return render_template('index.html')

@app.route('/success')
def success():
    emails = mysql.query_db ("SELECT email, DATE_FORMAT(created_at, '%M %e, %Y %H:%i') as date FROM friends")
    return render_template('success.html', all_emails=emails)
'''



