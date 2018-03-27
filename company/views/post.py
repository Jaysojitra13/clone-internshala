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

class PostView(TemplateView):
	template_name = 'company/existingpost.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['post_listt']  = PostDetails.objects.filter(company_id = self.request.user.id)
		return context

class ExistingPost(TemplateView):
	template_name = 'company/existingpost.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		CP = CompanyProfile.objects.get(user = self.request.user)
		PD = PostDetails.objects.filter(company_id = CP.user_id)

		context['company'] = CompanyProfile.objects.filter(user_id = CP.user_id)
		context['post'] = PostDetails.objects.filter(company_id = CP.user_id, status="live")
		return context

class AllPostView(TemplateView):
	template_name = 'company/allpost.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		CP = CompanyProfile.objects.get(user = self.request.user)
		PD = PostDetails.objects.filter(company_id = CP.user_id)

		context['company'] = CompanyProfile.objects.filter(user_id = CP.user_id)
		context['post'] = PostDetails.objects.filter(company_id = CP.user_id)
		return context


class PastPostView(TemplateView):
	template_name = 'company/pastpost.html'


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		CP = CompanyProfile.objects.get(user = self.request.user)
		PD = PostDetails.objects.filter(company_id = CP.user_id)

		context['company'] = CompanyProfile.objects.filter(user_id = CP.user_id)
		context['post'] = PostDetails.objects.filter(company_id = CP.user_id,status="end")
		return context