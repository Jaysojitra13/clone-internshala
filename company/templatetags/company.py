from django import template
from intern.models import *
from company.models import *

register = template.Library()

@register.filter(name="intern_name") 
def intern_name(value):
	q = PersonalDetails.objects.filter(internprofile_id = value)
	return q

@register.filter(name="post_name")
def post_name(value):
	q1 = PostDetails.objects.filter(id = value)
	return q1

@register.filter(name="academic_detail")
def academic_detail(value):
	q2 = AcademicDetails.objects.filter(internprofile_id = value)
	return q2

@register.filter(name="project_detail")
def project_detail(value):
	q3 = ProjectDetails.objects.filter(internprofile_id = value)
	return q3

@register.filter(name="upc_details")
def upc_details(value):
	q4 = UserPostConnection.objects.get(postdetails_id = value)
	return q4.status

@register.filter(name="upc_detailss")
def upc_detailss(value):
	q4 = UserPostConnection.objects.get(id = value)
	return q4.status