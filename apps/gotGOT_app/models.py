from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['firstNameLen'] = 'First name needs to be at least 2 letters long.'
        if not postData['first_name'].isalpha():
            errors['nameFormat'] = 'Name can only contain letters (no spaces).'

        if len(postData['last_name']) < 2:
            errors['lastNameLen'] = 'Last name needs to be at least 2 letters long.'
        if not postData['last_name'].isalpha():
            errors['nameFormat'] = 'Name can only contain letters (no spaces).'

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address.'
        if User.objects.filter(email = postData['email']):
            errors['emailInUse'] = 'Email address already in use.'

        if len(postData['password']) < 8 and len(postData['password']) > 20:
            errors['password'] = 'Password needs to be between 8 and 20 characters long.'
        if postData['password'] != postData['confirm']:
            errors['notPassword'] = 'Password does not match.'

        return errors

    def userValidator(self, postData):
        errors = {}
        try: 
            user = User.objects.get(email = postData['email'])
        except:
            errors['email'] = f'No email matching {postData["email"]}.'
            return errors

        if not bcrypt.checkpw(postData["password"].encode(), user.password.encode()):
            errors["password"] = "Password does not match email"

        return errors
    
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f'<User object: {self.first_name}, {self.last_name}, {self.email}, {self.password}, {self.created_at}, {self.updated_at}>'

class Event(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    time = models.DateTimeField()
    location = models.CharField(max_length=255)
    hosts = models.ForeignKey(User, related_name='hosts')
    joiners = models.ManyToManyField(User, related_name='joiners')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f'<User object: {self.title}, {self.genre}, {self.time}, {self.location}, {self.hosts}, {self.joiners}>'