from django import template 
from company.models import *
register = template.Library()


@register.filter(name='company_details')
def company_details(value):
	q = ContactDetails.objects.filter(company_id=value)
	return q

@register.filter(name='post_details')
def post_details(value):
	q1 = PostDetails.objects.filter(company_id = value)
	return q1

@register.filter(name='company_name')
def company_name(value):
	q2 = ContactDetails.objects.get(company_id = value)
	return q2.company_name

@register.filter(name='city_name')
def city_name(value):
	return ContactDetails.objects.all()

@register.filter(name='tech_name')
def tech_name(value):
	return PostDetails.objects.all()

@register.filter(name="messages")
def messages(value, upc_id):
	return Messages.objects.filter(postdetails_id=value, upc_id=upc_id)

@register.filter(name="messages_count")
def messages_count(value, upc_id):
	q3 = Messages.objects.filter(postdetails_id=value,upc_id=upc_id, is_read=False).count()
	return q3

@register.filter(name="pesonal_detail")
def personal_detail(value):
	PD_id = PersonalDetails.objects.get(internprofile_id=value)
	return PD_id.id

@register.filter(name="pesonal_detailid")
def personal_detailid(value):
	PD_id = PersonalDetails.objects.get(internprofile_id=value)
	return PD_id.id

@register.filter(name="check_test")
def check_test(value):
	check_test = TestApplicationMapping.objects.get(upc_id = value)
	return check_test.teststatus_id

