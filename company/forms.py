from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from .models import *
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field
from django.views.generic import FormView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

class CompanyForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username','email','password')

class ContactDetailsForm(forms.ModelForm):
	company_name = forms.CharField(label="Organization name", widget=forms.TextInput(attrs={'placeholder': 'Organization Name'}))	
	hr_fname = forms.CharField(label="HR's Fisrtname", widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
	hr_lname = forms.CharField(label="HR's Lastname", widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
	hr_email = forms.CharField(label="HR's Email-id", widget=forms.TextInput(attrs={'placeholder': 'Email-id'}))
	website_url = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'website URL'}))
	location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Location'}))
	contact_number = forms.RegexField(label="Mobile Number",regex=r'^\+?1?\d{9,15}$', widget=forms.TextInput(attrs={'placeholder': 'Contact Number'}),error_messages = {'invalid':"Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed."})
	class Meta:
		model = ContactDetails
		exculde= ('company')
		fields = ['company_name','hr_fname','hr_lname','hr_email','website_url','location','contact_number']
		def __init__(self, *args, **kwargs):
			super(PersonalDetailsForm, self).__init__(*args, **kwargs)
			self.helper.form_method = 'POST'
			self.helper.form_class = 'form-inline'
			self.helper.label_class = 'form-control'
			self.helper.field_class = 'form-control'
			self.helper.layout = Layout(
				Field('hr_fname', css_class='input-md'),
				Field('hr_lname', css_class='input-md'),
				Field('hr_email', css_class='input-md'),
				Field('website_url', css_class='input-md'),
				Field('location', css_class='input-md'),
				Field('contact_number', css_class='input-md'),
				
			)
			super(PersonalDetailsForm, self).__init__(*args, **kwargs)

TECHNOLOGY_CHOICES = (('','Select Technology'),('Java','Java'),('Test','Test'),('node','node'),('Python','Python'),('Android','Android'),('Ruby','Ruby'),('Ruby','Ruby'),('BD','BD'),('BI','BI'),('UX/UI design','UX/UI design'))
TYPE_CHOICES = (('','Select type'),('Full Time','Full Time'),('Part Time','Part Time'),('Work From Home','Work From Home'))


class PostDetailsForm(forms.ModelForm):
	domain = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'domain'}))
	technology = forms.ChoiceField(choices = TECHNOLOGY_CHOICES, widget=forms.Select(attrs={'class':'regDropDown'}))
	typeof_internship = forms.ChoiceField(choices = TYPE_CHOICES, widget=forms.Select(attrs={'class':'regDropDown'}))
	time_duration = forms.CharField(label='Time duration (In month)',widget=forms.TextInput(attrs={'placeholder': 'Time Duration'}))
	apply_by = forms.CharField(label='Last date to apply', widget=forms.TextInput(attrs={'placeholder': 'Apply by'}))
	stipend = forms.CharField(label='Stipend (per month)', required=False, widget=forms.TextInput(attrs={'placeholder': 'Stipend'}))	
	start_date = forms.DateField(label='Start date(YY-MM-DD)', widget=forms.TextInput(attrs={'placeholder': 'Start Date'}))
	numberof_interns = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'No. of integers'}))
	class Meta:
		model = PostDetails
		fields = ['domain','technology','numberof_interns','time_duration','stipend','start_date','apply_by','typeof_internship']
		def __init__(self, *args, **kwargs):
			super(PersonalDetailsForm, self).__init__(*args, **kwargs)
			self.helper.form_method = 'POST'
			self.helper.form_class = 'form-inline'
			self.helper.label_class = 'form-control'
			self.helper.field_class = 'form-control'
			self.helper.layout = Layout(
				Field('domain', css_class='input-md'),
				Field('technology', css_class='input-md'),
				Field('numberof_interns', css_class='input-md'),
				Field('time_duration', css_class='input-md'),
				Field('stipend', css_class='input-md'),
				Field('start_date', css_class='input-md'),
				Field('apply_by', css_class='input-md'),
				Field('typeof_internship', css_class='input-md'),
				
			)
			super(PersonalDetailsForm, self).__init__(*args, **kwargs)

# 	class QuestionForm(forms.ModelForm):
# 	text = forms.CharField(label="Question")
# 	class Meta:
# 		model = Question
# 		fields = ['text']
		
# class AnswerForm(forms.ModelForm):
# 	text = forms.CharField(label="Answer")
# 	class Meta:
# 		model = Answers
# 		fields = ['text']

# class CompanySignUpForm(UserCreationForm):
# 	class Meta(UserCreationForm.Meta):
# 		model = User

# 	def save(self):
# 		user = super().save(commit=False)
		
# 		user.is_copmany = True
# 		user.save()
# 		internprofile = InternProfile.objects.create(user=user)
# 		#internprofile.interests.add(*self.cleaned_data.get('interests'))
# 		return user	
 

 	