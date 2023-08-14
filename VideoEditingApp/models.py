from django.db import models
from django.contrib.auth.models import *

from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    changepw_otp=models.CharField(max_length=100,null=True,blank=True)
    is_verfied=models.BooleanField(default=False)
   

    def __str__(self):
        return self.username
    class Meta:
        app_label = 'VideoEditingApp' 

class Clips(models.Model):
    video = models.FileField(upload_to='clips/',blank=True, null=True)
    subclips=models.URLField(blank=True, null=True)
    title=models.CharField(blank=True, null=True,max_length=255)
    thumbnail_url= models.URLField( blank=True, null=True)

class VideoToAudio(models.Model):
  video = models.FileField(upload_to='videos/',blank=True, null=True)
  audio_url=models.URLField(blank=True, null=True)
  title=models.CharField(blank=True, null=True,max_length=255)

class Student(models.Model):  
    first_name = models.CharField(max_length=20)  
    last_name  = models.CharField(max_length=30)  
    roll_number=models.CharField(max_length=30)  
    class Meta:  
        db_table = "student" 

#one to one relationship model
class Profile(models.Model):
    age = models.IntegerField()
    address = models.CharField(max_length=200)

class Person(models.Model):
    name = models.CharField(max_length=100)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

class Products(models.Model):
    name=models.CharField(max_length=100)
    price=models.FloatField()
    quantity=models.CharField(max_length=100)