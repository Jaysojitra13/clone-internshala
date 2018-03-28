from intern.models import *
from company.models import *

class ListofQuestionViewService:

	def updateQuestion(self, question, answer, question_id):
		question_obj = Question.objects.get(id = question_id)
		answer_obj = AnswersHR.objects.get(question_id = question_id)
		question_obj.text = question
		question_obj.save()

		answer_obj.text = answer
		answer_obj.save()

		return response

	def addQuestion(self, self1, question, answer, tech):

		answer_obj1 = AnswersHR()
		question_obj1 = Question()
		question_obj1.text = question
		question_obj1.company_id = self1.request.user.id
		question_obj1.technology_id = tech.pk
		question_obj1.save()
		
		answer_obj1.question_id = question_obj1.pk
		answer_obj1.text = answer
		answer_obj1.save()

		return question_obj1, answer_obj1


class CreateTestViewService:

	def createTest(self, self1, upc_id, question_list):
		post_id = UserPostConnection.objects.get(id = upc_id).postdetails_id
		tech = PostDetails.objects.get(id = post_id).technology
		technology = Technology.objects.get(technology_name = tech).id
		test = Test()
		test.technology_id = technology
		test.save()
		ids = [Question.objects.get(text = question).id for question in question_list]
		objs = [QuestionTestMap() for i in question_list]
		for i in range(len(question_list)):
			objs[i].question_id = ids[i]
			objs[i].test_id = test.id
			objs[i].save()
		
		tam = TestApplicationMapping()
		tam.test_id = test.id
		tam.upc_id = upc_id
		tam.teststatus_id = 0
		tam.save()
		return 