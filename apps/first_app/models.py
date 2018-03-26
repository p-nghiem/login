from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
import sys, re
from datetime import date, datetime
from views import *

# Create your models here.

class UserManager(BaseUserManager):
    def Validator(self, postData):
        errors = {}
        #user = User.objects.get() # try this
        firstname = postData['firstname']
        lastname = postData['lastname']
        email = postData['email']
        password = postData['password']
        confirmpassword = postData['confirmpassword']
        birthday = postData['birthday']
        today = date.today()
        print ("today is", today)

        emailexists = User.objects.filter(email=email)

        if len(firstname) < 2 or firstname.isalpha() == False:        # Error first name
            errors['firstname'] = "First name must be at least 2 characters long, letters only"
        if len(lastname) < 2 or lastname.isalpha() == False:          # Error last name
            errors['lastname'] = "Last name must be at least 2 characters long, letters only"
        if not rejectEmail.match(email):                              # Error email format
            errors['email'] = "Email is not valid"
        if len(emailexists) > 0:
            errors['emailexists'] = "Email is already in use"
        # if not date.strftime(datetime.date(birthday), "%m/%d/%Y"):
        #    errors['birthdayformat'] = "Birthdate must be in the form MM/DD/YYYY" 
        # if time.strptime(birthday, "%d/%m/%Y") > time.strptime(today,"%d/%m/%Y") :
        #    errors['birthday'] = "Birthday cannot be in the future"
        # if datetime.date(birthday) > today:
        # if time.strptime(birthday, "%d/%m/%Y") > time.strptime(today,"%d/%m/%Y") :
        #   yourdatetime.date() < datetime.today().date()
        #    errors['birthday'] = "Birthday cannot be in the future"
        if len(password) < 8:                                         # Error password
            errors['passwordlength'] = "Password must be at least 8 characters long"
        if password != confirmpassword:                               # Error password match
            errors['passwordmatch'] = "Passwords do not match"
        return errors

    def Create_user(self, postData):
        email = postData['email']
        password = postData['password']
        user = self.model(email.self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

#       course = Course.objects.filter(name = postData['name'])

class Item(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    added_by_id = models.IntegerField()
    def __repr__(self):
        return "<Book object: {} {} {} {} {}>".format(self.name, self.desc, self.created_at, self.updated_at, self.uploaded_by_id)
'''
class User(models.Model):
    uploaded_books = models.ManyToManyField(Book, related_name="uploader")
    liked_books = models.ManyToManyField(Book, related_name="liked_users")
    def __repr__(self):
        return "<User object: {} {} {} {} {} {} {}>".format(self.first_name, self.last_name, self.email, self.created_at, self.updated_at, self.uploaded_books, self.liked_books)
'''

    
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    birthday = models.DateTimeField(blank=True, null=True)
    added_items = models.ManyToManyField(Item, related_name="item_adder")
    wished_for_items = models.ManyToManyField(Item, related_name="wished_for_by_users")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name, last_name'] #USERNAME_FIELD and password are required by default

    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

