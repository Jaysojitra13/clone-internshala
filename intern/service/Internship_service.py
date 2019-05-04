from intern.models import *
from company.models import * 

class InternshipDetailViewService:

	def internships(self, self1):
		tmp = ['tech','duration', 'stipend','city','typ']
		p = PostDetails.objects.all()
		
		for i in tmp:
			if i == 'tech': 
				if self1.request.GET.get('tech') != '' and self1.request.GET.get('tech') != None:
					self1.request.session['tech'] = self1.request.GET.get('tech')
					p = p.filter(technology=self1.request.GET.get('tech'))
				else:
					if 'tech' in self1.request.session:
						del self1.request.session['tech']
				
			
			if i == 'duration':
				if self1.request.GET.get('duration') != '' and self1.request.GET.get('duration') != None:
					self1.request.session['duration'] = self1.request.GET.get('duration')					
					p = p.filter(time_duration=self1.request.GET.get('duration'))
				else:
					if 'duration' in self1.request.session:
						del self1.request.session['duration']
						

			if i == 'stipend':
				if self1.request.GET.get('stipend') != '' and  self1.request.GET.get('stipend') != None:
					self1.request.session['stipend'] = self1.request.GET.get('stipend')
					p = p.filter(stipend__gt=0)
				else:
					if 'stipend' in self1.request.session:
						del self1.request.session['stipend']
						

			if i == 'city':
				contact = ContactDetails.objects.filter(location=self1.request.GET.get('city'))
				post = PostDetails.objects.all()
				if self1.request.GET.get('city') != '' and self1.request.GET.get('city') != None:
					self1.request.session['city'] = self1.request.GET.get('city')
					for i in contact:
						for j in post:
							p = p.filter(company_id = i.company_id)
				else:
					if 'city' in self1.request.session:
						del self1.request.session['city']

			if i== 'typ':
				if self1.request.GET.get('typ') != '' and self1.request.GET.get('typ') != None:
					self1.request.session['typ'] = self1.request.GET.get('typ')
					p = p.filter(typeof_internship=self1.request.GET.get('typ'))
				else:
					if 'typ' in self1.request.session:
						del self1.request.session['typ']
		return p

class InternPostConnectionService:

	def user_postconnection(self, request, id1, id2):
		obj = UserPostConnection()
				
		obj.company_id = CompanyProfile.objects.get(user = id1).pk
		obj.internprofile_id = request.user.id
		obj.postdetails_id = PostDetails.objects.get(id = id2).id
		obj.applied_date = datetime.datetime.now().date()
		obj.statusupdate_date = datetime.datetime.now().date()
		obj.save()

		return