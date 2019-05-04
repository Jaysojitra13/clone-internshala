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
from intern.service.testmodule_service import *
class GiveTestView(TemplateView):
	template_name = 'intern/give_test.html'
 
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		id = kwargs['pk']

		test = GiveTestViewService()
		questions = test.giveTest(id)

		context['questions'] = questions
		context['upc_id'] = kwargs['pk']
		return context

class SubmitTestView(View):

	def post(self, request, *args, **kwargs):

		test_submit = SubmitTestViewService()
		test_submit.submitTest(request)

		return HttpResponseRedirect('/intern/index/')

class ShowResultView(View):

	def get(self, request, *args, **kwargs):
		id = request.GET.get('upc_id')
		tam = TestApplicationMapping.objects.get(upc_id = id).result
		return JsonResponse({'result':tam},safe = False)