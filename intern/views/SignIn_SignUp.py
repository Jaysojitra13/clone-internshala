#import code; code.interact(local=dict(globals(), **locals()))
from django.views import View
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect, HttpResponse, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from intern.models import *
from company.models import *
from intern.forms import *
from company.forms import *
from django.forms.models import inlineformset_factory
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic import TemplateView
from django.views import generic
from django.urls import reverse_lazy
from allauth.account.views import * 
from allauth.socialaccount.models import * 
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf.urls import *
from django.db.models.query import QuerySet
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic.detail import SingleObjectMixin
import datetime
import json


def CheckUser(request, type):

	if type == "intern":
		request.session['user'] = 'intern'
		return HttpResponseRedirect('/accounts/signup/')

	elif type == "company":
		request.session['user'] = 'company'
		return HttpResponseRedirect('/accounts/signup/')


		
class MySignUpView(SignupView):
	# def form_valid(self, form):
	# 	return HttpResponseRedirect('/accounts/signup')

	def form_valid(self, form):
		#self.user = form.save(self.request)
		data = self.request.session.get('user')
		print(data)
		
		self.user = form.save(self.request)		

		if data == 'company':
			self.user.is_company = True
			self.user.save()
			
		return HttpResponseRedirect('/accounts/login/')

	
def CheckLogin(request, type):
	if type == "intern":
		request.session['user'] = 'intern'
		return HttpResponseRedirect('/accounts/login/')

	elif type == "company":
		request.session['user'] = 'company'
		return HttpResponseRedirect('/accounts/login/')


class MyLogInView(LoginView):

	def form_valid(self, form):
		data = self.request.session.get('user')
		
		print('login', data)
		if data == 'company':
			return HttpResponseRedirect('/company/contactdetail/')
		elif data == 'intern':
			return HttpResponseRedirect('/intern/index/')

	def post(self, request):
		PD = PersonalDetails.objects.all()
		AD = AcademicDetails.objects.all()		
		CD = ContactDetails.objects.all()
		user = authenticate(username=self.request.POST.get('login'),password=self.request.POST.get('password'))
		login(request, user)
		if not user is None:
			if user.is_company:
				for i in CD:
					if i.company_id == self.request.user.id:
						return HttpResponseRedirect('/company/applications/')
				return HttpResponseRedirect('/company/contactdetail/')
			else:
				for i in PD:					
					if i.internprofile_id == self.request.user.id:
						return HttpResponseRedirect('/intern/index/')
				return HttpResponseRedirect('/intern/personaldetail/')
		return HttpResponseRedirect('/accounts/login/')

