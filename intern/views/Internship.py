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
from intern.service.Internship_service import *

class InternshipDetailView(TemplateView):
	model = PostDetails
	
	template_name = 'intern/internship.html'
	

	
	def get_context_data(self, **kwargs):
			data = dict()
			page = self.request.GET.get('page')

			if AcademicDetails.objects.filter(internprofile_id = self.request.user.id).exists():
				data['AD'] = AcademicDetails.objects.get(internprofile_id = self.request.user.id).pk

			if PersonalDetails.objects.filter(internprofile_id = self.request.user.id).exists():
				data['PD'] = PersonalDetails.objects.get(internprofile_id = self.request.user.id).pk
	
	
	
			internship = InternshipDetailViewService()
			p = internship.internships(self)
			

			data['data']=p
			paginator = Paginator(p, 3)
			data['data'] = paginator.get_page(page)
			return data
		
			

	

class InternPostConnection(SingleObjectMixin, TemplateView):
	
	def get(self, request, *args, **kwargs):
		
		self.object = self.request.user

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
				
				upc = InternPostConnectionService()
				upc.user_postconnection(request, id1, id2)
				
				return HttpResponseRedirect('/intern/internship')
		else:

			return HttpResponseRedirect('/accounts/login/')
	



def ReadMessages(request,id):
	upc_details = UserPostConnection.objects.filter(postdetails_id=id)
	
	for upc in upc_details:
		Messages.objects.filter(postdetails_id=upc.postdetails_id).update(is_read="True")

	return HttpResponse(status = 200)

