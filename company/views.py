#import code; code.interact(local=dict(globals(), **locals()))
from django.views import View
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from intern.views import *
from intern.models import *
from company.forms import *
from django.forms.models import inlineformset_factory
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
import datetime
# Create your views here.

class ContactDetailsView(CreateView):
	model = ContactDetails
	form_class = ContactDetailsForm
	template_name = 'company/contact_detail.html'
	success_url = reverse_lazy('company:index')
	def form_valid(self, form):
		print('CD')
		CP = CompanyProfile.objects.get(user = self.request.user)
		PF = form.save(commit=False)
		PF.company = CP
		PF.save()
		return super(ContactDetailsView, self).form_valid(form)

class PostDetailsView(CreateView):
	model = PostDetails
	form_class = PostDetailsForm
	template_name = 'company/post_detail.html'
	success_url = reverse_lazy('company:all-post')
	def form_valid(self, form):
		print('CPD')
		CP = CompanyProfile.objects.get(user = self.request.user)
		PF = form.save(commit=False)
		PF.company = CP
		return super(PostDetailsView, self).form_valid(form)



class Index(TemplateView):
	template_name = 'company/index.html'

	

class ExistingPost(ListView):
	template_name = 'company/existingpost.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		CP = CompanyProfile.objects.get(user = self.request.user)
		#PD = PostDetails.objects.filter(company_id = CP.user_id)
		return PostDetails.objects.filter(company_id = CP.user_id, status="live")


	# def get_context_data(self, **kwargs):
	# 	CP = CompanyProfile.objects.get(user = self.request.user)
	# 	PD = PostDetails.objects.filter(company_id = CP.user_id)

	# 	context['company'] = CompanyProfile.objects.get(user_id = CP.user_id)
	# 	context['post'] = PostDetails.objects.get(company_id = CP.user_id)
	# 	return context

class ApplicationView(TemplateView):
	template_name = 'company/application.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		applied_date = self.request.GET.get('ddid')
		print(applied_date)
		page = self.request.GET.get('page')
		domain = self.request.GET.get('domain')
		date = self.request.GET.get('date')
		post = PostDetails.objects.filter(domain=domain)
		#	import code; code.interact(local=dict(globals(), **locals()))	
		CP = CompanyProfile.objects.get(user = self.request.user)
		if applied_date == '1':
			applicants = UserPostConnection.objects.filter(company_id = CP.user_id).order_by(	'-applied_date')	
		else:
			applicants = UserPostConnection.objects.filter(company_id = CP.user_id).order_by('-id')

		tmp = ['domain','date']

		for i in tmp:
			if i == 'domain':
				if self.request.GET.get('domain') != '' and self.request.GET.get('domain') != None:
					self.request.session['domain'] = self.request.GET.get('domain')
					for j in post:
						
						applicants = applicants.filter(postdetails_id = j.id).order_by('-applied_date')
						
				else:
					if 'domain' in self.request.session:
						del self.request.session['domain']

			if i == 'date':
				if self.request.GET.get('date') != '' and self.request.GET.get('date') != None:
					applicants = applicants.filter(applied_date = self.request.GET.get('date'))
				else:
					if 'date' in self.request.session:
						del self.request.session['date']
					
			
		# context['MEDIA_URL'] =  settings.MEDIA_URL
		# context['MEDIA_ROOT'] =  settings.MEDIA_ROOT
		context['applicants'] = applicants
		paginator = Paginator(applicants, 50)
		context['applicants'] = paginator.get_page(page)
		return context

class MessageView(TemplateView):
		
	
	def get(self, request, *args, **kwargs):
		idd = request.GET.get('idd')
		upc_id = request.GET.get('upc_id')
			
		obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = idd)
		
		print(obj)
		obj.status = "Accepted"
		obj.statusupdate_date = datetime.datetime.now().date()
		obj.save()
		return HttpResponseRedirect('/company/applications')
	
class SaveMsg(TemplateView):

	def get(self, request, *args, **kwargs):
		data = request.GET.get('message')
		post_idd = request.GET.get('post_id')
		upc_id = request.GET.get('upc_id')	
		obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = post_idd )
		obj.status="InProcess"
		obj.statusupdate_date = datetime.datetime.now().date()
		obj.save()
		obj1 = Messages()
		obj1.postdetails_id = post_idd
		obj1.messages = data
		obj1.message_date = datetime.datetime.now().date()
		obj1.save()
		return HttpResponseRedirect('/company/applications')

class ViewDetails(TemplateView):
	template_name = 'company/viewdetail.html'

	def get_context_data(self, 	**kwargs):
		
		context = super().get_context_data(**kwargs)
		pk = kwargs['id']
		CP = CompanyProfile.objects.get(user = self.request.user)
		context = super().get_context_data(**kwargs)
		applicants = UserPostConnection.objects.filter(company_id = CP.user_id)
		context['pk'] = pk
		context['applicants'] = applicants
		return context

class RejectView(TemplateView):
	def get(self, request, *args, **kwargs):
		idd = request.GET.get('idd')
		upc_id = request.GET.get('upc_id')
		data = request.GET.get('rejectMsg')
		obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = idd)
		obj.status="Rejected"
		obj.statusupdate_date = datetime.datetime.now().date()
		obj.save()
		obj1 = Messages()
		obj1.postdetails_id = idd
		obj1.messages = data
		obj1.save()
		return HttpResponseRedirect('/company/applications/')

class ConfirmView(TemplateView):
	def get(self, request, *args, **kwargs):
		idd = request.GET.get('idd')
		upc_id = request.GET.get('upc_id')
		
		obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = idd)
		obj.status="Confirmed"
		obj.statusupdate_date = datetime.datetime.now().date()
		obj.save()
		return HttpResponseRedirect('/company/applications/')

class ConfirmInternView(TemplateView):
	template_name = 'company/confirmintern.html'

	def get_context_data(self, 	**kwargs):
			
		context = super().get_context_data(**kwargs)
		company_id = kwargs['pk']
		context['upc'] = UserPostConnection.objects.filter(company_id= kwargs['pk'],status="Confirmed") 
		return context

class PostView(TemplateView):
	template_name = 'company/post.html'



class AllPostView(ListView):
	template_name = 'company/allpost.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		CP = CompanyProfile.objects.get(user = self.request.user)
		print('ALLpost views')
		#PD = PostDetails.objects.filter(company_id = CP.user_id)
		return PostDetails.objects.filter(company_id = CP.user_id)


class PastPostView(ListView):
	template_name = 'company/pastpost.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		CP = CompanyProfile.objects.get(user = self.request.user)
		print('ALLpost views')
		#PD = PostDetails.objects.filter(company_id = CP.user_id)
		return PostDetails.objects.filter(company_id = CP.user_id, status="end")

class ListofInternView(TemplateView):
	template_name = 'company/listintern.html'

class RejectInternView(TemplateView):
	template_name = 'company/rejectintern.html'

	def get_context_data(self, 	**kwargs):
			
		context = super().get_context_data(**kwargs)
		company_id = kwargs['pk']
		context['upc'] = UserPostConnection.objects.filter(company_id= kwargs['pk'],status="Rejected") 
		return context