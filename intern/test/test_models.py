from django.test import TestCase
from intern.models import User, PersonalDetails
# Create your tests here.

class UserTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		user = User.objects.create(username="Ali",email="Ali@gmail.com")
		personal_detail = PersonalDetails.objects.create(internprofile_id = user.id,email="ali@gamil.com",contact_number="123",current_city="Ahemdabad",second_city="surat", name="ali")

	def test_first_name(self):
		PD = PersonalDetails.objects.get(id=1) 
		field_label = PD._meta.get_field('name').verbose_name
		self.assertEqual(field_label, 'name')

	def test_email(self):
		PD = PersonalDetails.objects.get(id=1)
		field_label = PD._meta.get_field('email').verbose_name
		self.assertEqual(field_label, 'email')

	def test_contact_number(self):
		PD = PersonalDetails.objects.get(id=1)
		max_length = PD._meta.get_field('contact_number').max_length
		self.assertEqual(max_length, 10)