from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from intern.models import InternProfile
from django.contrib.auth.models import AbstractUser
from django.conf import settings

User = get_user_model()
# Create your models here.
class CompanyProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='company_profile')

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
	print('****', created)
	
	CompanyProfile.objects.get_or_create(user = instance)
	
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
	# data= request.session.get('user')
	# print("@nd",data)
	instance.company_profile.save()


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
	start_date = models.DateTimeField()
	apply_by = models.DateTimeField()
	typeof_internship = models.CharField(max_length=20)

class UserPostConnection(models.Model):
	internprofile = models.ForeignKey(InternProfile, on_delete=models.CASCADE)
	company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
	postdetails = models.ForeignKey(PostDetails, on_delete=models.CASCADE)
	status = models.CharField(max_length=25)
	
class Messages(models.Model):
	postdetails = models.ForeignKey(PostDetails, on_delete=models.CASCADE)
	messages = models.TextField(max_length=500)
	is_read = models.BooleanField(default= False)