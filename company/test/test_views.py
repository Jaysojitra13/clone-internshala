from django.test import TestCase, Client
from intern.models import *
from company.models import *
from django.urls import reverse

import datetime
class ComapnyApplicationView(TestCase):
		
	@classmethod
	def setUp(self):
		# import code; code.interact(local=dict(globals(), **locals()))
		user_intern = [User.objects.create_user(username='testuser'+str(i), password="12345", email="aa"+str(i)+"@gmail.com") for i in range(0,3)]


		# test_user1 = User.objects.create_user(username='testuser1', password="12345", email="a@gmail.com")
		user_company = User.objects.create_user(username='testuser', password="12345", email="b@gmail.com", is_company=True)

		for i in range(len(user_intern)):
			personal_detail = PersonalDetails.objects.create(internprofile_id = user_intern[i].id,email="ali"+str(i)+"@gamil.com",contact_number="123",current_city="Ahemdabad",second_city="surat", name="ali")

			academic_detail = AcademicDetails.objects.create(internprofile_id = user_intern[i].id, schoolname_10="a",percentage_10="12",marksheet_10="dfs",schoolname_12="as",percentage_12="234", marksheet_12="sasdg" ,college_name="sdfds" ,current_year="2", marksheet_clg="dsgadsg" ,cpi="8")

			project_detail = ProjectDetails.objects.create(internprofile_id = user_intern[i].id,title="Adfa",typeof_project="asdfads",description= "sdgasD",project_link="https://123.com")

		company_contactdetail = ContactDetails.objects.create(company_id = user_company.id,company_name="Ads",hr_fname="a",hr_lname="b",hr_email="ad@das.com" ,website_url="https://123.com" ,location= "ad" ,contact_number="1123456789")

		

		company_post = [PostDetails.objects.create(company_id = user_company.id,domain="as"+str(i),technology="AS",numberof_interns="3",time_duration="2" ,stipend="212",start_date=datetime.datetime.now().date(),apply_by=datetime.datetime.now().date(),typeof_internship="fae",status="2") for i in range(len(user_intern))]

		upc = [UserPostConnection.objects.create(status = "0", company_id=user_company.id, internprofile_id = user_intern[1].id,postdetails_id = company_post[i].id, applied_date ="2018-04-1"+str(i), statusupdate_date = datetime.datetime.now().date()) for i in range(len(company_post))]




	def test_redirect_if_not_logged_in(self):
		resp = self.client.get(reverse('company:applications'))
		self.assertRedirects(resp, '/accounts/login/?next=/company/applications/')
		


	def test_logged_in_uses_correct_template(self):
		login = self.client.login(username= 'testuser', password='12345')
		resp = self.client.get(reverse('company:applications'))
		company_profile = InternProfile.objects.get(pk=4)
		applicants = UserPostConnection.objects.filter(company_id = company_profile.user_id).order_by('id')
		# import code; code.interact(local=dict(globals(), **locals()))
		self.assertEqual(len(resp.context['applicants']),UserPostConnection.objects.count())
		self.assertEqual(len(resp.context['data']),PostDetails.objects.count())
		self.assertTemplateUsed(resp, 'company/application.html')
		
	
