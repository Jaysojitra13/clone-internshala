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