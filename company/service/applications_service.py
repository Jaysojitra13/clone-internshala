from intern.models import *
from company.models import *
 
class AplicationViewService:

	def applications(self, self1):
		di = dict([('domain', self1.request.GET.get('domain')),('applied_datedesc',self1.request.GET.get('token_datedesc')),('applied_dateasc',self1.request.GET.get('token2_dateasc')),('name_desc',self1.request.GET.get('token_namedesc') ),('name_asc',self1.request.GET.get('token2_nameasc')),('page',self1.request.GET.get('page')),('date',self1.request.GET.get('date'))])
		return di

	def sorted_applicants(self, self1, applied_datedesc, applied_dateasc, name_desc, name_asc, domain, date):
		company_profile = CompanyProfile.objects.get(user = self1.request.user)
		applicants = UserPostConnection.objects.filter(company_id = company_profile.user_id).order_by('id')
		post = PostDetails.objects.filter(technology = domain)

		if applied_dateasc == '2':
			applicants = UserPostConnection.objects.filter(company_id = company_profile.user_id).order_by('applied_date')
		elif applied_datedesc == '1':
			applicants = UserPostConnection.objects.filter(company_id = company_profile.user_id).order_by('-applied_date')
		elif name_desc == "1":
			applicants = UserPostConnection.objects.filter(company_id = company_profile.user_id).order_by('-internprofile__personal_details__name')
		elif name_asc == "2":
			applicants = UserPostConnection.objects.filter(company_id = company_profile.user_id).order_by('internprofile__personal_details__name')
		else:
			applicants = UserPostConnection.objects.filter(company_id = company_profile.user_id).order_by('id')
			if 'domain' in self1.request.session:
				del self1.request.session['domain']

		if domain == '' and date != '':	
			applicants = applicants.filter(applied_date = self1.request.GET.get('date'))
			
		elif domain != '' and date == '':
			self1.request.session['domain'] = domain
			for j in post:
				applicants = applicants.filter(postdetails_id = j.id).order_by('-applied_date')
		elif domain != '' and date != '':
			for j in post:
				applicants = applicants.filter(applied_date = self1.request.GET.get('date'),postdetails_id = j.id).order_by('-applied_date')
		
		return applicants


class ViewApplicationService:

	def viewApplication(self, self1):
		CP = CompanyProfile.objects.get(user = self1.request.user)
		applicants = UserPostConnection.objects.filter(company_id = CP.user_id)
		return applicants


class RejectViewService:

	def rejectIntern(self, post_id, upc_id, reject_msg):
		upc_obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = post_id)
		upc_obj.status= 3
		upc_obj.statusupdate_date = datetime.datetime.now().date()
		upc_obj.save()
		message_obj1 = Messages()
		message_obj1.postdetails_id = post_id
		message_obj1.messages = reject_msg
		message_obj1.upc_id = upc_id
		message_obj1.save()
		return 

class ConfirmViewService:

	def confirmIntern(self, post_id, upc_id):
		upc_obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = post_id)
		upc_obj.status= 4
		upc_obj.statusupdate_date = datetime.datetime.now().date()
		upc_obj.save()
		return 
