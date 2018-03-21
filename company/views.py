# import code; code.interact(local=dict(globals(), **locals()))
from django.views import View
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.template.loader import render_to_string
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
from django.forms.formsets import formset_factory
import datetime 
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers

# Create your views here.


class ContactDetailsView(CreateView):
	model = ContactDetails
	form_class = ContactDetailsForm
	template_name = 'company/contact_detail.html'
	success_url = reverse_lazy('company:index')
	def form_valid(self, form):
		print('CD')
		company_profile = CompanyProfile.objects.get(user = self.request.user)
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

	



class ApplicationView(TemplateView):
	template_name = 'company/application.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		applied_datedesc = self.request.GET.get('token_datedesc')
		applied_dateasc = self.request.GET.get('token2_dateasc')
		name_desc = self.request.GET.get('token_namedesc')
		name_asc = self.request.GET.get('token2_nameasc')
		page = self.request.GET.get('page')
		domain = self.request.GET.get('domain')
		date = self.request.GET.get('date')
		post = PostDetails.objects.filter(domain=domain)
		#	import code; code.interact(local=dict(globals(), **locals()))	
		company_profile = CompanyProfile.objects.get(user = self.request.user)

		if applied_dateasc == '2':
			applicants = UserPostConnection.objects.filter(company_id = company_profile.user_id).order_by('applied_date')
		elif applied_datedesc == '1':
			applicants = UserPostConnection.objects.filter(company_id = company_profile.user_id).order_by('-applied_date')
		elif self.request.GET.get('token_namedesc') == "1":
			applicants = UserPostConnection.objects.filter(company_id = company_profile.user_id).order_by('-internprofile__personal_details__name')
		elif self.request.GET.get('token2_nameasc') == "2":
			applicants = UserPostConnection.objects.filter(company_id = company_profile.user_id).order_by('internprofile__personal_details__name')
		else:
			applicants = UserPostConnection.objects.filter(company_id = company_profile.user_id).order_by('id')

		# tmp = ['domain','date']

		# for i in tmp:
		# 	if i == 'domain':
		# 		if self.request.GET.get('domain') != '' and self.request.GET.get('domain') != None:
		# 			self.request.session['domain'] = self.request.GET.get('domain')
		# 			for j in post:
		# 				applicants = applicants.filter(postdetails_id = j.id).order_by('-applied_date')
						
		# 		else:
		# 			if 'domain' in self.request.session:
		# 				del self.request.session['domain']

		# 	if i == 'date':
		# 		if self.request.GET.get('date') != '' and self.request.GET.get('date') != None:
		# 			self.request.session['date'] = self.request.GET.get('date')
		# 			applicants = applicants.filter(applied_date = self.request.GET.get('date'))
		# 		else:
		# 			if 'date' in self.request.session:
		# 				del self.request.session['date']
					
		if domain == '' and date != '':	
			applicants = applicants.filter(applied_date = self.request.GET.get('date'))
		elif domain != '' and date == '':
			for j in post:
				applicants = applicants.filter(postdetails_id = j.id).order_by('-applied_date')
		elif domain != '' and date != '':
			for j in post:
				applicants = applicants.filter(applied_date = self.request.GET.get('date'),postdetails_id = j.id).order_by('-applied_date')
		
			
	
		context['applicants'] = applicants
		paginator = Paginator(applicants, 50)
		context['applicants'] = paginator.get_page(page)
		return context

class MessageView(TemplateView):
		
	
	def get(self, request, *args, **kwargs):
		idd = request.GET.get('idd')
		upc_id = request.GET.get('upc_id')
			
		obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = idd)
		
		print(obj)
		obj.status = "Accepted"
		obj.statusupdate_date = datetime.datetime.now().date()
		obj.save()

		response = JsonResponse({'post_id':request.GET.get('idd'), 'upc_id': request.GET.get('upc_id')}, safe = False)
		return response
	
class SaveMsg(TemplateView):

	def get(self, request, *args, **kwargs):
		data = request.GET.get('message')
		post_idd = request.GET.get('post_id')
		upc_id = request.GET.get('upc_id')	
		obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = post_idd )
		obj.status="InProcess"
		obj.statusupdate_date = datetime.datetime.now().date()
		obj.save()
		obj1 = Messages()
		obj1.postdetails_id = post_idd
		obj1.messages = data
		obj1.message_date = datetime.datetime.now().date()
		obj1.save()
		return HttpResponseRedirect('/company/applications')

class ViewDetails(TemplateView):
	template_name = 'company/viewdetail.html'

	def get_context_data(self, 	**kwargs):
		
		context = super().get_context_data(**kwargs)
		pk = kwargs['id']
		CP = CompanyProfile.objects.get(user = self.request.user)
		context = super().get_context_data(**kwargs)
		applicants = UserPostConnection.objects.filter(company_id = CP.user_id)
		context['pk'] = pk
		context['applicants'] = applicants
		return context

class RejectView(TemplateView):
	def get(self, request, *args, **kwargs):
		idd = request.GET.get('idd')
		upc_id = request.GET.get('upc_id')
		data = request.GET.get('rejectMsg')
		obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = idd)
		obj.status="Rejected"
		obj.statusupdate_date = datetime.datetime.now().date()
		obj.save()
		obj1 = Messages()
		obj1.postdetails_id = idd
		obj1.messages = data
		obj1.save()
		return HttpResponseRedirect('/company/applications/')

class ConfirmView(TemplateView):
	def get(self, request, *args, **kwargs):
		idd = request.GET.get('idd')
		upc_id = request.GET.get('upc_id')
		
		obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = idd)
		obj.status="Confirmed"
		obj.statusupdate_date = datetime.datetime.now().date()
		obj.save()
		return HttpResponseRedirect('/company/applications/')

class ConfirmInternView(TemplateView):
	template_name = 'company/confirmintern.html'

	def get_context_data(self, 	**kwargs):
			
		context = super().get_context_data(**kwargs)
		company_id = kwargs['pk']
		context['upc'] = UserPostConnection.objects.filter(company_id= kwargs['pk'],status="Confirmed") 
		return context

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

class ListofInternView(TemplateView):
	template_name = 'company/listintern.html'

class RejectInternView(TemplateView):
	template_name = 'company/rejectintern.html'

	def get_context_data(self, 	**kwargs):
			
		context = super().get_context_data(**kwargs)
		company_id = kwargs['pk']
		context['upc'] = UserPostConnection.objects.filter(company_id= kwargs['pk'],status="Rejected") 
		return context

class GenerateQuestionView(TemplateView):
	template_name = 'company/test.html'

	def get_context_data(self, 	**kwargs):
		context = super().get_context_data(**kwargs)
		context['technology'] = Technology.objects.all()
		return context 

	def post(self, request, *args, **kwargs):
		return HttpResponseRedirect('/company/addquestion/')

class ListofQuestionView(TemplateView):
	template_name = 'company/addquestion.html'

	def get_context_data(self, 	**kwargs):
		context = super().get_context_data(**kwargs)
		context['technology'] = Technology.objects.all()
		tech = Technology.objects.get(technology_name = kwargs['type'])
		context['type'] = kwargs['type']
		context['questions'] = Question.objects.filter(technology_id = tech.pk)
		context['answers'] = Answers_HR.objects.all()
		return context

	def post(self,request, *args, **kwargs):
		try:
			question = request.POST.get('question')
			answer = request.POST.get('answer')
			print("before IF")
			if request.POST.get('question') != "" and request.POST.get('answer') != "":

				tech = Technology.objects.get(technology_name = kwargs['type'])
				print("TEchnology is",tech)
				obj1 = Answers_HR()
				obj = Question()
				obj.text = question
				obj.company_id = request.user.id
				obj.technology_id = tech.pk
				obj.save()

				
				obj1.question_id = obj.pk
				obj1.text = answer
				obj1.save()
				print("obj is ---------------",obj)
				response = JsonResponse({'obj_id': obj.id,'obj_text':obj.text,'obj_technologyid':obj.technology_id,'obj1_text':obj1.text},safe =False)
				
				return  response
		except Exception as e:
			print(e)

class GenerateTestView(TemplateView):
	template_name = "company/generateTest.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		idd = kwargs['id']
		# print(idd)
		upc = UserPostConnection.objects.get(id=kwargs['id']).postdetails_id
		post = PostDetails.objects.get(id = upc).technology
		tech = Technology.objects.get(technology_name = post)
		context['questions'] = Question.objects.filter(company_id = self.request.user.id, technology_id= tech)
		print(post)
		context['upc_id'] = kwargs['id']
		# print(upc)
		return context

class CreateTestView(View):
	# template_name = "company/createtest.html"

	# def get(self, request, *args, **kwargs):
	# 	upc_id = request.GET.get('upc_id')
	# 	print("upc_id",upc_id)
	# 	question_list = request.GET.getlist('checkboxes')

	# 	return HttpResponseRedirect('/company/applications/')

	def post(self, request, *args, **kwargs):
		upc_id = request.POST.get('upc_id')
		question_list = request.POST.getlist('checkboxes')
		post_id = UserPostConnection.objects.get(id = upc_id).postdetails_id
		tech = PostDetails.objects.get(id = post_id).technology
		technology = Technology.objects.get(technology_name = tech).id
		test = Test()
		test.technology_id = technology
		test.save()
		ids = [Question.objects.get(text = question).id for question in question_list]
		objs = [QuestionTestMap() for i in question_list]
		for i in range(len(question_list)):
			objs[i].question_id = ids[i]
		for i in range(len(question_list)):
			objs[i].test_id = test.id
		for i in objs:
			i.save()
		tam = TestApplicationMapping()
		tam.test_id = test.id
		tam.upc_id = request.POST.get('upc_id')
		tam.teststatus_id = 0
		tam.save()

		return HttpResponseRedirect('/company/applications/')

class ResultView(TemplateView):
	template_name = 'company/result.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		upc_id = kwargs['id']
		context['answers_intern'] = Answers_intern.objects.filter(upc_id = kwargs['id'])
		tam_testid = TestApplicationMapping.objects.get(upc_id = kwargs['id']).test_id
		qtm = list(QuestionTestMap.objects.filter(test_id = tam_testid))
		questions = []
		for i in range(len(qtm)):
			if qtm[i].question_id == Question.objects.get(id = qtm[i].question_id).id:
				questions.append(Question.objects.get(id = qtm[i].question_id))
		# import code; code.interact(local=dict(globals(), **locals()))
		context['questions'] = questions
		context['upc_id'] = kwargs['id']
		return context

class CheckAnswerView(View):

	def get(self, request, *args, **kwargs):
		question_id = request.GET.get('question_id')
		# import code; code.interact(local=dict(globals(), **locals()))
		answer_intern = Answers_intern.objects.get(question_id = request.GET.get('question_id'))
		if request.GET.get('right') == 'right':
			answer_intern.is_correct = True
			answer_intern.save()
		elif request.GET.get('wrong') == 'wrong':
			answer_intern.is_correct = False
			answer_intern.save()
		return HttpResponseRedirect("/company/result/"+request.GET.get('upc_id')+"")

class CountResultView(View):
	def get(self, request, *args, **kwargs):
		upc_id = request.GET.get('upc_id')
		all_answers = Answers_intern.objects.filter(upc_id = request.GET.get('upc_id')).count()
		right_answers = Answers_intern.objects.filter(upc_id = request.GET.get('upc_id'),is_correct = True).count()
		tap =  TestApplicationMapping.objects.get(upc_id = request.GET.get('upc_id'))
		marks = round((right_answers *100 / all_answers), 2) 
		tap.result = marks
		tap.teststatus_id = 2
		tap.save()
		# import code; code.interact(local=dict(globals(), **locals()))
		return JsonResponse({'marks': marks}, safe=False)