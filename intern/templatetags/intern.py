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
def messages(value):
	q3 = Messages.objects.filter(postdetails_id=value)
	return q3

@register.filter(name="messages_count")
def messages_count(value):
	q3 = Messages.objects.filter(postdetails_id=value,is_read=False).count()
	return q3
@register.filter(name="pesonal_detail")
def personal_detail(value):
	PD_id = PersonalDetails.objects.get(internprofile_id=value)
	return PD_id.id
# @register.filter(name="is_read")
# def is_read(value):
# 	MessageObj = Messages.objects.get(postdetails_id=value)
# 	return MessageObj.is_read