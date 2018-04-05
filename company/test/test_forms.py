from django.test import TestCase, Client
from company.forms import *

class ContactDetailFormTest(TestCase):
	def test_contact_detail_form_label(self):
		form = ContactDetailsForm()
		self.assertTrue(form.fields['company_name'].label == 'Organization name')

