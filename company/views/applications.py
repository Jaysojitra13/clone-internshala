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
from company.service.applications_service import *

class ApplicationView(TemplateView):
	template_name = 'company/application.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		application  = AplicationViewService()
		di = application.applications(self)
		applied_datedesc = di['applied_datedesc']
		applied_dateasc = di['applied_dateasc']
		name_desc = di['name_desc'] 
		name_asc = di['name_asc']
		page = di['page']
		domain = di['domain']
		date = di['date']
		post = PostDetails.objects.filter(technology = domain)
		applicants = application.sorted_applicants(self, applied_datedesc, applied_dateasc, name_desc, name_asc, domain, date)

		context['data'] = PostDetails.objects.all()	
		context['applicants'] = applicants
		paginator = Paginator(applicants, 50)
		context['applicants'] = paginator.get_page(page)
		return context

class ViewDetails(TemplateView):
	template_name = 'company/viewdetail.html'

	def get_context_data(self, 	**kwargs):
		
		context = super().get_context_data(**kwargs)
		pk = kwargs['id']

		intern_detail = ViewApplicationService()
		applicants = intern_detail.viewApplication(self)
	
		context['pk'] = pk
		context['applicants'] = applicants
		return context

class RejectView(TemplateView):
	def get(self, request, *args, **kwargs):
		post_id = request.GET.get('idd')
		upc_id = request.GET.get('upc_id')
		reject_msg = request.GET.get('rejectMsg')

		reject_intern = RejectViewService()
		reject_intern.rejectIntern(post_id, upc_id, reject_msg)

		return HttpResponseRedirect('/company/applications/')

class ConfirmView(TemplateView):
	def get(self, request, *args, **kwargs):
		post_id = request.GET.get('idd')
		upc_id = request.GET.get('upc_id')
		
		confirm_intern = ConfirmViewService()
		confirm_intern.confirmIntern(post_id, upc_id)
		# upc_obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = post_id)
		# upc_obj.status="Confirmed"
		# upc_obj.statusupdate_date = datetime.datetime.now().date()
		# upc_obj.save()
		return HttpResponseRedirect('/company/applications/')

class ConfirmInternView(TemplateView):
	template_name = 'company/confirmintern.html'

	def get_context_data(self, 	**kwargs):
			
		context = super().get_context_data(**kwargs)
		company_id = kwargs['pk']
		context['upc'] = UserPostConnection.objects.filter(company_id= kwargs['pk'],status="Confirmed") 
		return context

class RejectInternView(TemplateView):
	template_name = 'company/rejectintern.html'

	def get_context_data(self, 	**kwargs):
			
		context = super().get_context_data(**kwargs)
		company_id = kwargs['pk']
		context['upc'] = UserPostConnection.objects.filter(company_id= kwargs['pk'],status="Rejected") 
		return context

class ListofInternView(TemplateView):
	template_name = 'company/listintern.html'