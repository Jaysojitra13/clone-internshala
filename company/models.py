from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages

from django.contrib.auth.models import AbstractUser
from django.conf import settings
import intern
import datetime

class CompanyProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='company_profile')

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_profile(sender, instance, created, **kwargs):
# 	print('****', created)
# 	print('company',instance.is_company)
# 	if instance.is_company == 'True':
# 		CompanyProfile.objects.get_or_create(user = instance)
# 	else:
# 		intern.models.InternProfile.objects.get_or_create(user= instance)


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
# 	# data= request.session.get('user')
# 	# print("@nd",data)
# 	if instance.is_company == 'True':
# 		instance.company_profile.save()
# 	else:
# 		intern.models.InternProfile.objects.get_or_create(user= instance)

class ContactDetails(models.Model):
	company = models.OneToOneField(CompanyProfile, on_delete=models.CASCADE)
	company_name = models.CharField(max_length=30)
	hr_fname = models.CharField(max_length=20)
	hr_lname = models.CharField(max_length=20)
	hr_email = models.EmailField()
	website_url = models.URLField()
	location = models.CharField(max_length=50)
	contact_number = models.BigIntegerField()

class PostDetails(models.Model):
	company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
	domain = models.CharField(max_length=20)
	technology = models.CharField(max_length=20)
	numberof_interns = models.IntegerField()
	time_duration = models.IntegerField() 
	stipend = models.IntegerField()
	start_date = models.DateField()
	apply_by = models.DateField()
	typeof_internship = models.CharField(max_length=20)
	status = models.CharField(max_length=10,default="live")

class UserPostConnection(models.Model):
	internprofile = models.ForeignKey(intern.models.InternProfile, on_delete=models.CASCADE)
	company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
	postdetails = models.ForeignKey(PostDetails, on_delete=models.CASCADE)
	status = models.CharField(max_length=25,default="Applied")
	applied_date = models.DateField()
	statusupdate_date = models.DateField()
	
class Messages(models.Model):
	postdetails = models.ForeignKey(PostDetails, on_delete=models.CASCADE)
	messages = models.TextField(max_length=500)
	is_read = models.BooleanField(default= False)
	message_date = models.DateField(default=datetime.datetime.now().date())

class Technology(models.Model):
	technology_name = models.CharField(max_length=10)

class Question(models.Model):
	technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
	company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)		
	text = models.CharField(max_length=50)

class Answers_HR(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	text = models.CharField(max_length=20)

class Answers_intern(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	text = models.CharField(max_length=20)
	upc = models.ForeignKey(UserPostConnection,on_delete=models.CASCADE)
	is_correct = models.BooleanField(default=True)

class Test(models.Model):
	technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
	creation_date = models.DateField(default=datetime.datetime.now().date())

class QuestionTestMap(models.Model):
	test = models.ForeignKey(Test, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)

class TestApplicationMapping(models.Model):
	upc = models.ForeignKey(UserPostConnection, on_delete=models.CASCADE)
	test = models.ForeignKey(Test, on_delete=models.CASCADE)