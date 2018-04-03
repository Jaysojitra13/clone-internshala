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
from company.service.testmodule_service import *

class GenerateQuestionView(TemplateView):
	template_name = 'company/addquestion.html'

	def get_context_data(self, 	**kwargs):
		context = super().get_context_data(**kwargs)
		context['technology'] = Technology.objects.all()
		return context 

	

class ListofQuestionView(TemplateView):
	template_name = 'company/addquestion.html'

	def get_context_data(self, 	**kwargs):
		context = super().get_context_data(**kwargs)
		context['technology'] = list(Technology.objects.all())
		tech = Technology.objects.get(technology_name = kwargs['type'])
		context['type'] = kwargs['type']
		context['check'] = "question"

		context['questions'] = Question.objects.filter(technology_id = tech.pk, company_id = self.request.user.id).order_by('id')
		context['answers'] = AnswersHR.objects.all()
		return context

	def post(self,request, *args, **kwargs):

		try: 
			question = request.POST.get('question')
			answer = request.POST.get('answer')
			question_id = request.POST.get('question_id')

			if question_id:
				
				update_question = ListofQuestionViewService()
				response = update_question.updateQuestion(question, answer, question_id)
				response = JsonResponse({'obj_id': question_obj.id,'obj_text':question_obj.text,'obj_technologyid':question_obj.technology_id,'obj1_text':answer_obj.text},safe =False)
				
				return  response

			else: 

				tech = Technology.objects.get(technology_name = kwargs['type'])

				add_question = ListofQuestionViewService()
				question_obj1, answer_obj1 = add_question.addQuestion(self, question, answer, tech)
				
				response = JsonResponse({'obj_id': question_obj1.id,'obj_text':question_obj1.text,'obj_technologyid':question_obj1.technology_id,'obj1_text':answer_obj1.text},safe =False)
				return  response
		except Exception as e:
			return HttpResponseRedirect('/company/applications/')		

class GenerateTestView(TemplateView):
	template_name = "company/generateTest.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# upc_id = kwargs['id']
		upc = UserPostConnection.objects.get(id=kwargs['id']).postdetails_id
		context['check'] = "app"
		post = PostDetails.objects.get(id = upc).technology
		tech = Technology.objects.get(technology_name = post)
		context['questions'] = Question.objects.filter(company_id = self.request.user.id, technology_id= tech)
		context['upc_id'] = kwargs['id']
		context['technology'] = tech
		return context

class CreateTestView(View):

	def post(self, request, *args, **kwargs):
		upc_id = request.POST.get('upc_id')
		question_list = request.POST.getlist('checkboxes')

		create_test = CreateTestViewService()
		create_test.createTest(self, upc_id, question_list)

		return HttpResponseRedirect('/company/applications/')

class ResultView(TemplateView):
	template_name = 'company/result.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		upc_id = kwargs['id']
		context['AnswersIntern'] = AnswersIntern.objects.filter(upc_id = kwargs['id'])
		
		result = ResultViewService()
		questions = result.show_result(upc_id)
		
		context['questions'] = questions
		context['upc_id'] = kwargs['id']
		return context

class CheckAnswerView(View):

	def get(self, request, *args, **kwargs):
		
		answer = CheckAnswerViewService()
		answer.check_answer(request)
	
		return JsonResponse({'status':"OK"},safe=False)

class CountResultView(View):
	def get(self, request, *args, **kwargs):
		upc_id = request.GET.get('upc_id')

		result = CountResultViewService()
		marks = result.countResult(request)


		return JsonResponse({'marks': marks}, safe=False)

class DeleteOneQuestionView(View):
	def get(self, request, *args, **kwargs):
		question = Question.objects.get(id = request.GET.get('question_id')).delete()
		return JsonResponse({'status':"OK"},safe=False)

class DeleteAllQuestionView(View):
	def get(self, request, *args, **kwargs):
		question_list = request.GET.getlist('questions')
		for id in question_list:
			Question.objects.get(id = id).delete()
		return JsonResponse({'status':"OK"},safe=False)