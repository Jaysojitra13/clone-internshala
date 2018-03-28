# import code; code.interact(local=dict(globals(), **locals()))
import datetime 
from django.views import View
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.forms.models import inlineformset_factory
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.formsets import formset_factory
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers
from company.forms import *
from intern.views import *
from intern.models import *
from company.models import *

class ContactDetailsView(CreateView):
	model = ContactDetails
	form_class = ContactDetailsForm
	template_name = 'company/contact_detail.html'
	success_url = reverse_lazy('company:applications')
	def form_valid(self, form):
		company_profile=CompanyProfile.objects.get(user = self.request.user)
		PF = form.save(commit=False)
		PF.company = company_profile
		PF.save()
		return super(ContactDetailsView, self).form_valid(form)

class PostDetailsView(CreateView):
	model = PostDetails
	form_class = PostDetailsForm
	template_name = 'company/post_detail.html'
	success_url = reverse_lazy('company:all-post')
	def form_valid(self, form):
		print('CPD')
		company_profile = CompanyProfile.objects.get(user = self.request.user)
		PF = form.save(commit=False)
		PF.company = company_profile
		PF.save()
		return super(PostDetailsView, self).form_valid(form)



class Index(TemplateView):
	template_name = 'company/index.html'	