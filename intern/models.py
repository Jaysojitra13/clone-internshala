from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.contrib import messages
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager, AbstractBaseUser
from django.contrib.auth.decorators import login_required
# Create your models here.


# class MyUserManager(UserManager):
# 	def create_user(self, is_company, password=None):
# 		user = self.model(
# 				is_company = True
# 			)
# 		user.save(using=self._db)
# 		return user
class User(AbstractUser):
	is_company = models.BooleanField(default= False)

	REQUIRED_FIELDS = ['email']

class InternProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='intern_profile',primary_key=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	print('****', created)
	
	InternProfile.objects.get_or_create(user = instance)
	
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	# data= request.session.get('user')
	# print("@nd",data)
	instance.intern_profile.save()

class PersonalDetails(models.Model):
	internprofile = models.OneToOneField(InternProfile, on_delete=models.CASCADE, related_name='personal_details')
	name = models.CharField(max_length=25)
	email = models.EmailField(max_length=25)
	contact_number = models.BigIntegerField()
	current_city = models.CharField(max_length=25)
	second_city = models.CharField(max_length=25)

class AcademicDetails(models.Model):
	internprofile = models.OneToOneField(InternProfile, on_delete=models.CASCADE)
	schoolname_10 = models.CharField(max_length=30)
	percentage_10 = models.FloatField()
	marksheet_10 = models.FileField()
	schoolname_12 = models.CharField(max_length=30)
	percentage_12 = models.FloatField()
	marksheet_12 = models.FileField()
	college_name = models.CharField(max_length=50)
	current_year = models.IntegerField()
	marksheet_clg = models.FileField()
	cpi = models.FloatField()

class ProjectDetails(models.Model):
	internprofile = models.ForeignKey(InternProfile, on_delete=models.CASCADE)
	title = models.CharField(max_length=20)
	typeof_project = models.CharField(max_length=20)
	description = models.TextField(max_length=500)
	project_link = models.URLField()
