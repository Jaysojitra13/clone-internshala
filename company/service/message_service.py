from intern.models import *
from company.models import *
from django.http import JsonResponse

class MessageViewService:
	def message(self, post_id, upc_id):
		upc_obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = post_id)
		upc_obj.status = "1"
		upc_obj.statusupdate_date = datetime.datetime.now().date()
		upc_obj.save()
		return 

class SaveMsgService:
	def saveMessage(self, data, post_id, upc_id):
		upc_obj = UserPostConnection.objects.get(id=upc_id,postdetails_id = post_id)
		upc_obj.status = 2
		upc_obj.statusupdate_date = datetime.datetime.now().date()
		upc_obj.save()
		
		message_obj1 = Messages()
		message_obj1.postdetails_id = post_id
		message_obj1.messages = data
		message_obj1.message_date = datetime.datetime.now().date()
		message_obj1.upc_id = upc_id
		message_obj1.save()
		return