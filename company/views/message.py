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
from company.service.message_service import *

class MessageView(TemplateView):
		
	
	def get(self, request, *args, **kwargs):
		post_id = request.GET.get('idd')
		upc_id = request.GET.get('upc_id')
		
		message = MessageViewService()
		message.message(post_id, upc_id)
		response = JsonResponse({'post_id':self.request.GET.get('idd'), 'upc_id': self.request.GET.get('upc_id')}, safe = False)

		return response
	
class SaveMsg(TemplateView):

	def get(self, request, *args, **kwargs):
		data = request.GET.get('message')
		post_id = request.GET.get('post_id')
		upc_id = request.GET.get('upc_id')	

		save_message = SaveMsgService()
		save_message.saveMessage(data, post_id, upc_id)

		return HttpResponseRedirect('/company/applications')