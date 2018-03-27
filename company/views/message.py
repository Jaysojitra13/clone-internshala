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

class MessageView(TemplateView):
		
	
	def get(self, request, *args, **kwargs):
		post_id = request.GET.get('idd')
		upc_id = request.GET.get('upc_id')
			
		upc_obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = post_id)
		
		upc_obj.status = "Accepted"
		upc_obj.statusupdate_date = datetime.datetime.now().date()
		upc_obj.save()

		response = JsonResponse({'post_id':request.GET.get('idd'), 'upc_id': request.GET.get('upc_id')}, safe = False)
		return response
	
class SaveMsg(TemplateView):

	def get(self, request, *args, **kwargs):
		data = request.GET.get('message')
		post_id = request.GET.get('post_id')
		upc_id = request.GET.get('upc_id')	
		upc_obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = post_id)
		upc_obj.status="InProcess"
		upc_obj.statusupdate_date = datetime.datetime.now().date()
		upc_obj.save()
		message_obj1 = Messages()
		message_obj1.postdetails_id = post_id
		message_obj1.upc_id = upc_id
		message_obj1.messages = data
		message_obj1.message_date = datetime.datetime.now().date()
		message_obj1.save()
		return HttpResponseRedirect('/company/applications')