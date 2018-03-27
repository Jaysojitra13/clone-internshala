from django import template
from intern.models import *
from company.models import *

register = template.Library()

@register.filter(name="intern_name") 
def intern_name(value):
	personalDetail = PersonalDetails.objects.filter(internprofile_id = value)
	return personalDetail

@register.filter(name="post_name")
def post_name(value):
	postDetail = PostDetails.objects.filter(id = value)
	return postDetail

@register.filter(name="academic_detail")
def academic_detail(value):
	academicDetail = AcademicDetails.objects.filter(internprofile_id = value)
	return academicDetail

@register.filter(name="project_detail")
def project_detail(value):
	projectDetail = ProjectDetails.objects.filter(internprofile_id = value)
	return projectDetail

@register.filter(name="upc_details")
def upc_details(value):
	upc_post = UserPostConnection.objects.get(postdetails_id = value)
	return upc_post.status

@register.filter(name="upc_detailss")
def upc_detailss(value):
	q4 = UserPostConnection.objects.get(id = value)
	return q4.status

@register.filter(name="post_nameee")
def post_name(value):
	postDetail = PostDetails.objects.filter(company_id = value)
	return postDetail


@register.filter(name="questiontest_mapping")
def questiontest_mapping(value):
	qam =  QuestionTestMap.objects.filter(test_id = value)
	return qam

@register.filter(name="question_text")
def question_text(value):
	question =  Question.objects.get(id = value)
	return question

@register.filter(name="answer_intern")
def answer_intern(value,upc_id):
	answer_intern =  AnswersIntern.objects.filter(question_id = value,upc_id = upc_id)
	return answer_intern
	

@register.filter(name="answer_internexist")
def answer_internexist(value):
	question =  AnswersIntern.objects.filter(upc_id = value)
	return question

@register.filter(name="answer_hr")
def answer_hr(value):
	AnswerHR =  AnswersHR.objects.filter(question_id = value)
	return AnswerHR	

@register.filter(name="test_appmapping")
def test_appmapping(value):
	tap = TestApplicationMapping.objects.get(upc_id = value).result
	return tap

@register.filter(name="check_answer")
def check_answer(value):
	check_answer = AnswersIntern.objects.get(id = value).is_correct
	return check_answer

@register.filter(name="check_teststatus")
def check_teststatus(value):
	check_teststatus = TestApplicationMapping.objects.get(upc_id = value)
	return check_teststatus.teststatus_id

@register.filter(name="check_upcid")
def check_upcid(value):
	ans = answer_intern(value)
	answer_intern = AnswersIntern.objects.get(upc_id= value)
	return answer_intern.upc_id

