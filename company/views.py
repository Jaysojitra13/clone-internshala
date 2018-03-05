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
	success_url = reverse_lazy('company:index')
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
		return PostDetails.objects.filter(company_id = CP.user_id)


	# def get_context_data(self, **kwargs):
	# 	CP = CompanyProfile.objects.get(user = self.request.user)
	# 	PD = PostDetails.objects.filter(company_id = CP.user_id)

	# 	context['company'] = CompanyProfile.objects.get(user_id = CP.user_id)
	# 	context['post'] = PostDetails.objects.get(company_id = CP.user_id)
	# 	return context

class ApplicationView(TemplateView):
	template_name = 'company/application.html'

	def get_context_data(self, **kwargs):
		page = self.request.GET.get('page')
		IP = InternProfile.objects.get(user = self.request.user)
		context = super().get_context_data(**kwargs)
		applicants = UserPostConnection.objects.filter(company_id = IP.user_id)
		context['applicants'] = applicants
		paginator = Paginator(applicants, 2)
		context['applicants'] = paginator.get_page(page)
		return context

class MessageView(TemplateView):
		
	
	def get(self, request, *args, **kwargs):
		
		idd = request.GET.get('idd')
		
		obj = UserPostConnection.objects.get(postdetails_id = idd)
		obj.status = "Accepted"
		obj.save()
		return HttpResponseRedirect('/company/applications')
	
class SaveMsg(TemplateView):

	def get(self, request, *args, **kwargs):
		data = request.GET.get('message')
		post_idd = request.GET.get('post_id')

		obj1 = Messages()
		obj1.postdetails_id = post_idd
		obj1.messages = data
		obj1.save()
		return HttpResponseRedirect('/company/applications')