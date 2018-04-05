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

def InternProfileView(request):
	 
	#profile_form = InternProfileForm()
	if request.method == 'POST':
		user_form = UserForm(request.POST, prefix='UF')
		#profile_form = InternProfileForm(request.POST, prefix='PF')
		if user_form.is_valid():
			user = user_form.save(commit=False) 
			# profile = profile_form.save(commit = False)
			user.save()

		else:
			messages.error(request,("correct erroe=rs"))
	else:
		#import code; code.interact(local=dict(globals(), **locals()))

		user_form = UserForm(prefix='UF')
		#profile_form = InternProfileForm(prefix='PF')
		#print('hello')
	return render(request, 'intern/profile.html',{
			'user_form': user_form,
			#'profile_form': profile_form,
		})


class Home(TemplateView):
	
	template_name = 'intern/home1.html'
	def dispatch(self, request, *args, **kwargs):
		# if 'company' in request.session:
		# 	print('not there')	
		# super(Home, self).dispatch(request, *args, **kwargs)
		return super(Home, self).dispatch(request, *args, **kwargs)

class PersonalDetailView(CreateView):

	model = PersonalDetails
	#fields = ('name','email','contact_number','current_city','second_city')
	form_class = PersonalDetailsForm
	template_name  = 'intern/personal_detail.html'
	success_url = reverse_lazy('intern:academic-detail')

	def form_valid(self, form):
		print('PD')
		IP = InternProfile.objects.get(user = self.request.user)
		PF = form.save(commit=False)
		PF.internprofile = IP
		return super(PersonalDetailView, self).form_valid(form)

class UpdatePersonalDetailView(UpdateView):
	model = PersonalDetails
	form_class = PersonalDetailsForm
	template_name  = 'intern/personal_detail.html'
	success_url = reverse_lazy('intern:index')	
	
	def dispatch(self, *args, **kwargs):
		#or put some logic here
		print(kwargs['pk'])
		if kwargs['pk'] == '':
			return HttpResponseRedirect('/intern/personaldetail/')
		
		return super(UpdatePersonalDetailView, self).dispatch(*args, **kwargs)
	
	

class AcademicDetailView(CreateView):
	model = AcademicDetails
	#fields = ['schoolname_10','percentage_10','schoolname_12','percentage_12','college_name','current_year','cpi']
	form_class = AcademicDetailsForm
	template_name = 'intern/academic_detail.html'
	success_url = reverse_lazy('intern:project-detail')
	
	def form_valid(self, form):
		IP = InternProfile.objects.get(user = self.request.user)
		PF = form.save(commit=False)
		PF.internprofile = IP
		return super(AcademicDetailView, self).form_valid(form)
	
class UpdateAcademicDetailView(UpdateView):
	model = AcademicDetails
	form_class = AcademicDetailsForm
	template_name = 'intern/academic_detail.html'
	success_url = reverse_lazy('intern:index')

	def dispatch(self, *args, **kwargs):
		#or put some logic here
		if kwargs['pk'] == '':
			return HttpResponseRedirect('/intern/academicdetail/')
		
		return super(UpdateAcademicDetailView, self).dispatch(*args, **kwargs)

class ProjectDetailView(CreateView):
	model = ProjectDetails
	#fields = ['title','typeof_project','description','project_link']
	form_class = ProjectDetailsForm
	template_name = 'intern/project_detail.html'
	success_url = reverse_lazy('intern:index')

	def form_valid(self, form):
		
		IP = InternProfile.objects.get(user = self.request.user)
		PF = form.save(commit=False)
		PF.internprofile = IP
		return super(ProjectDetailView, self).form_valid(form)

class HomeView(TemplateView):
	template_name = 'intern/index.html'
	context_object_name = 'interns'
	
	def get_context_data(self, **kwargs):
		page = self.request.GET.get('page')
		IP = InternProfile.objects.get(user = self.request.user)
		context = super().get_context_data(**kwargs)
		if AcademicDetails.objects.filter(internprofile_id = self.request.user.id).exists():
			context['AD'] = AcademicDetails.objects.get(internprofile_id = self.request.user.id).pk

		if PersonalDetails.objects.filter(internprofile_id = self.request.user.id).exists():
			context['PD'] = PersonalDetails.objects.get(internprofile_id = self.request.user.id).pk
	
		upc= UserPostConnection.objects.filter(internprofile_id = IP.user_id).order_by('-id')
		context['upc'] = upc
		paginator = Paginator(upc, 10)
		context['upc'] = paginator.get_page(page)
		return context