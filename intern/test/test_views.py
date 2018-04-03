from django.test import TestCase, Client
from intern.models import *
from company.models import *
from django.urls import reverse

import datetime
class InternIndexView(TestCase):

	@classmethod
	def setUp(self):
		test_user1 = User.objects.create_user(username='testuser1', password="12345", email="a@gmail.com")
		test_user2 = User.objects.create_user(username='testuser2', password="12345", email="b@gmail.com", is_company=True)
		personal_detail = PersonalDetails.objects.create(internprofile_id = test_user1.id,email="ali@gamil.com",contact_number="123",current_city="Ahemdabad",second_city="surat", name="ali")

		academic_detail = AcademicDetails.objects.create(internprofile_id = test_user1.id, schoolname_10="a",percentage_10="12",marksheet_10="dfs",schoolname_12="as",percentage_12="234", marksheet_12="sasdg" ,college_name="sdfds" ,current_year="2", marksheet_clg="dsgadsg" ,cpi="8")

		project_detail = ProjectDetails.objects.create(internprofile_id=test_user1.id,title="Adfa",typeof_project="asdfads",description= "sdgasD",project_link="https://123.com")

		company_contactdetail = ContactDetails.objects.create(company_id = test_user2.id,company_name="Ads",hr_fname="a",hr_lname="b",hr_email="ad@das.com" ,website_url="https://123.com" ,location= "ad" ,contact_number="1123456789")

		company_post = PostDetails.objects.create(company_id = test_user2.id,domain="as",technology="AS",numberof_interns="3",time_duration="2" ,stipend="212",start_date=datetime.datetime.now().date(),apply_by=datetime.datetime.now().date(),typeof_internship="fae",status="2")

	def test_redirect_if_not_logged_in(self):
		resp = self.client.get(reverse('company:applications'))
		self.assertRedirects(resp, '/accounts/login/?next=/company/applications/')


	def test_logged_in_uses_correct_template(self):
		
		login = self.client.login(username= 'testuser2', password='12345')
		resp = self.client.get(reverse('company:applications'))
		self.assertEqual(str(resp.context['user']), 'testuser2')
		self.assertTemplateUsed(resp, 'company/application.html')
			
