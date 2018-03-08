from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from .models import *
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.forms import UserCreationForm

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
	email = forms.CharField(label="Email ID")
	contact_number = forms.RegexField(label="Mobile Number",regex=r'^\+?1?\d{9,15}$',error_messages = {'invalid':"Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed."})
	second_city = forms.CharField(label="2 city")
	def __init__(self, *args, **kwargs):
			super(PersonalDetailsForm, self).__init__(*args, **kwargs)
			self.helper = FormHelper()
			self.helper.form_method = 'POST'
			self.helper.form_class = 'form-horizontal'
			self.helper.label_class = 'col-md-2' 
			self.helper.field_class = 'col-md-8'
			self.helper.layout = Layout(
				Field('name'),
				Field('email'),
				Field('conatact_number'),
				Field('current_city'),
				Field('second_city'),
				
			)
			
			super(PersonalDetailsForm, self).__init__(*args, **kwargs)
	class Meta:
		model = PersonalDetails
		fields = ['name','email','contact_number','current_city','second_city']
		
			
class AcademicDetailsForm(forms.ModelForm):
	class Meta:
		model = AcademicDetails 
		fields = ['schoolname_10','percentage_10','marksheet_10','schoolname_12','percentage_12','marksheet_12', 'college_name','current_year','cpi','marksheet_clg']
		def __init__(self, *args, **kwargs):
			super(PersonalDetailsForm, self).__init__(*args, **kwargs)
			self.helper.form_method = 'POST'
			self.helper.form_class = 'form-horizontal'
			self.helper.label_class = 'control-label col-sm-5'
			self.helper.field_class = 'form-control'
			self.helper.layout = Layout(
				Field('schoolname_10'),
				Field('percentage_10'),
				Field('marksheet_10'),
				Field('schoolname_12'),
				Field('schoolname_12'),
				Field('marksheet_12'),
				Field('college_name'),
				Field('current_year'),
				Field('cpi'),
				Field('marksheet_clg'),
				
			)
			
			super(AcademicDetailsForm, self).__init__(*args, **kwargs)

class ProjectDetailsForm(forms.ModelForm):
	project_link = forms.URLField(required = False)
	class Meta:
		model = ProjectDetails
		fields = ['title','typeof_project','description','project_link']
		def __init__(self, *args, **kwargs):
			super(PersonalDetailsForm, self).__init__(*args, **kwargs)
			self.helper.form_method = 'POST'
			self.helper.form_class = 'form-horizontal'
			self.helper.label_class = 'control-label col-sm-5'
			self.helper.field_class = 'form-control'
			self.helper.layout = Layout(
				Field('title', css_class='input-sm'),
				Field('typeof_project', css_class='input-sm'),
				Field('conatact_number', css_class='input-sm'),
				Field('description', css_class='input-sm'),
				Field('project_link', css_class='input-sm'),
				
			)
			super(ProjectDetailsForm, self).__init__(*args, **kwargs)

class InternSignUpForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User

	def save(self):
		user = super().save(commit=False)
		print('VALID')
		user.is_company = True

		user.save()
		print('VALID1234')
		internprofile = InternProfile.objects.create(user=user)
		#internprofile.interests.add(*self.cleaned_data.get('interests'))
		return user	

class FilterForm(forms.Form):
	location = forms.CharField(label="Choose City")
	technology = forms.CharField(label="Choose technology")
	stipend = forms.BooleanField(label="Stipend")