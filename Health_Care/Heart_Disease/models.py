from django.db import models
from django.contrib.auth.models import User

from datetime import datetime  
class register_table(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    usertype=models.CharField(max_length=20,null=False,blank=False)
    contact_number = models.IntegerField()
    profile_pic =models.ImageField(upload_to = "profiles",null=True,blank=True)
    age = models.CharField(max_length=250,null=True,blank=True)
    city = models.CharField(max_length=250,null=True,blank=True)
    gender = models.CharField(max_length=250,default="Male")

    def __str__(self):
        return self.user.username
class subscribe(models.Model):
    email=models.CharField(max_length=100,blank=False)
    def __str__(self):
        return self.email
class Heart_Disease(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    city=models.CharField(max_length=100)
    age=models.IntegerField()
    sex=models.IntegerField()
    cp=models.IntegerField()
    trestbps=models.IntegerField()
    chol=models.IntegerField()
    fbs=models.IntegerField()
    restecg=models.IntegerField()
    thalach=models.IntegerField()
    exang=models.IntegerField()
    oldpeak=models.IntegerField()
    slope=models.IntegerField()
    ca=models.IntegerField()
    thal=models.IntegerField()
    Date=models.DateTimeField(auto_now=True)
    result=models.IntegerField()
    def __str__(self):
        return self.user.username
class feedbackd(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    experience=models.CharField(max_length=20)
    comment=models.TextField()
    date=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()
    def __str__(self):
        return self.name
