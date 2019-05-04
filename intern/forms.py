from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from .models import *
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Textarea
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

class UserForm(forms.ModelForm):
	
	class Meta:
		model = User
		fields = ('username','email','password') 

# class InternProfileForm(forms.ModelForm):
# 	class Meta:
# 		model = InternProfile
# 		fields = ['bio','location']

class PersonalDetailsForm(forms.ModelForm):
	name = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'Name'}))
	email = forms.CharField(label="Email ID",  widget=forms.TextInput(attrs={'placeholder': 'Email-id'}))
	contact_number = forms.RegexField(label="Mobile Number", widget=forms.TextInput(attrs={'placeholder': 'Contact Number'}) ,regex=r'^\+?1?\d{9,15}$',error_messages = {'invalid':"Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed."})
	current_city = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'Current City'}))
	second_city = forms.CharField(label="2 city",  widget=forms.TextInput(attrs={'placeholder': 'Second city'}))
	
	class Meta:
		model = PersonalDetails
		fields = ['name','email','contact_number','current_city','second_city']
		
			
class AcademicDetailsForm(forms.ModelForm):
	schoolname_10 = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'SchoolName 10'}))
	schoolname_12 = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'SchoolName 12'}))
	percentage_10 = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'Percentage 10'}))
	percentage_12 = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'Percentage 12'}))
	college_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'College Name'}))
	current_year = 	forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Current Year'}))
	cpi = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Current CPI'}))

	class Meta:
		model = AcademicDetails 
		fields = ['schoolname_10','percentage_10','marksheet_10','schoolname_12','percentage_12','marksheet_12', 'college_name','current_year','cpi','marksheet_clg']
		

class ProjectDetailsForm(forms.ModelForm):
	project_link = forms.URLField(required = False)
	title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Project Title'}))
	typeof_project = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type of Project'}))
	# description = 	forms.TextArea( widget=forms.TextInput(attrs={'placeholder': 'Description'}))
	project_link = 	forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'project Link'}))
	class Meta:
		model = ProjectDetails
		fields = ['title','typeof_project','description','project_link']
		
			

class InternSignUpForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User

	def save(self):
		user = super().save()
		user.is_company = True

		user.save()
		internprofile = InternProfile.objects.create(user=user)
		#internprofile.interests.add(*self.cleaned_data.get('interests'))
		return user	

