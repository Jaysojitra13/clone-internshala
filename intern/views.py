
#import code; code.interact(local=dict(globals(), **locals()))
from django.views import View
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect, HttpResponse, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
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

			# user.intern_profile.bio = profile_form.cleaned_data.get('bio')
			# user.intern_profile.location = profile_form.cleaned_data.get('location')
			# user.intern_profile.save()
			#profile.user = user
			# for inline_form in profile_form:
			# 	if inline_form.cleaned_data:
			# 		choice = inline_form.save(commit=False)
			#profile.save()
			# temp_profile = InternProfile.objects.get(user= user.id)
			# temp_profile.bio = profile.bio
			# temp_profile.location = profile.location
			#profile.user = user
			#temp_profile.save()
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
	
	template_name = 'intern/home.html'



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
	print('hh')
	# def get(self, request, *args, **kwargs):

	# 	print(kwargs['pk'])
	# 	if kwargs['pk'] == None:
	# 		return HttpResponseRedirect('/intern/index/')
	# 	else:
	# 		return HttpResponseRedirect('/intern/updatepersonaldetail/'+ kwargs['pk']+'')
	# 	return HttpResponseRedirect('/intern/index/')
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
		print('PD')
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
		print(kwargs['pk'])
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
		
		print('POD')
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
		paginator = Paginator(upc, 5)
		context['upc'] = paginator.get_page(page)
		return context

	
	# def get_absolute_url(self): 
	# 	return reverse("intern/index.html")

 

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
		print('login')
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


class InternshipDetailView(TemplateView):
	model = PostDetails
	
	template_name = 'intern/internship.html'
	

	
	def get_context_data(self, **kwargs):
			data = dict()

		
	
			city = self.request.GET.get('city')
			tech = self.request.GET.get('tech')
			stipend =  self.request.GET.get('stipend')
			duration =  self.request.GET.get('duration')
			typ = self.request.GET.get('typ')
			page = self.request.GET.get('page')
	
			tmp = ['tech','duration', 'stipend','city','typ']
			p = PostDetails.objects.all()
			
			for i in tmp:
				if i == 'tech': 
					if self.request.GET.get('tech') != '' and self.request.GET.get('tech') != None:
						self.request.session['tech'] = self.request.GET.get('tech')
						p = p.filter(technology=self.request.GET.get('tech'))
					else:
						if 'tech' in self.request.session:
							del self.request.session['tech']
					
				
				if i == 'duration':
					if self.request.GET.get('duration') != '' and self.request.GET.get('duration') != None:
						self.request.session['duration'] = self.request.GET.get('duration')					
						p = p.filter(time_duration=self.request.GET.get('duration'))
					else:
						if 'duration' in self.request.session:
							del self.request.session['duration']
							

				if i == 'stipend':
					if self.request.GET.get('stipend') != '' and  self.request.GET.get('stipend') != None:
						self.request.session['stipend'] = self.request.GET.get('stipend')
						p = p.filter(stipend__gt=0)
					else:
						if 'stipend' in self.request.session:
							del self.request.session['stipend']
							

				if i == 'city':
					contact = ContactDetails.objects.filter(location=self.request.GET.get('city'))
					post = PostDetails.objects.all()
					if self.request.GET.get('city') != '' and self.request.GET.get('city') != None:
						self.request.session['city'] = self.request.GET.get('city')
						for i in contact:
							for j in post:
								p = p.filter(company_id = i.company_id)
					else:
						if 'city' in self.request.session:
							del self.request.session['city']

				if i== 'typ':
					if self.request.GET.get('typ') != '' and self.request.GET.get('typ') != None:
						self.request.session['typ'] = self.request.GET.get('typ')
						p = p.filter(typeof_internship=self.request.GET.get('typ'))
					else:
						if 'typ' in self.request.session:
							del self.request.session['typ']	

			data['data']=p
			paginator = Paginator(p, 3)
			data['data'] = paginator.get_page(page)
			return data
		
			

	

class InternPostConnection(SingleObjectMixin, TemplateView):
	
	def get(self, request, *args, **kwargs):
		
		self.object = self.request.user
		print(self.object.id)

		if self.object.id != None:
			id1 = kwargs['company_id']
			id2 = kwargs['post_id']
			if PersonalDetails.objects.filter(internprofile_id= self.object.id).exists() == False:
				
				return HttpResponseRedirect('/intern/personaldetail/')	

			if UserPostConnection.objects.filter(company_id=id1, internprofile_id= self.object.id,postdetails_id=id2).exists():
				return HttpResponseRedirect('/intern/internship/')
			else:
				id1 = kwargs['company_id']
				id2 = kwargs['post_id']
				obj = UserPostConnection()
				
				obj.company_id = CompanyProfile.objects.get(user = id1).pk
				obj.internprofile_id = request.user.id
				obj.postdetails_id = PostDetails.objects.get(id = id2).id
				obj.applied_date = datetime.datetime.now().date()
				obj.statusupdate_date = datetime.datetime.now().date()
				obj.save()
				return HttpResponseRedirect('/intern/internship')
		else:

			return HttpResponseRedirect('/accounts/login/')
	



def ReadMessages(request,id):
	upc_details = UserPostConnection.objects.filter(postdetails_id=id)
	
	for upc in upc_details:
		Messages.objects.filter(postdetails_id=upc.postdetails_id).update(is_read="True")

	return HttpResponse(status = 200)