from intern.models import *
from company.models import *

class GiveTestViewService:

	def giveTest(self, id):
		tam_test_id = TestApplicationMapping.objects.get(upc_id = id).test_id
		qtm = list(QuestionTestMap.objects.filter(test_id = tam_test_id))
		questions = []
		for i in range(len(qtm)):
			if qtm[i].question_id == Question.objects.get(id = qtm[i].question_id).id:
				questions.append(Question.objects.get(id = qtm[i].question_id))

		return questions

class SubmitTestViewService:
	
	def submitTest(self, request):
		id = request.POST.get('upc_id')
		answers_list = request.POST.getlist('answers')

		objs = [AnswersIntern() for i in answers_list]
		test = TestApplicationMapping.objects.get(upc_id = id)
		test.teststatus_id = 1
		test.save()
		qtm = QuestionTestMap.objects.filter(test_id = test.test_id)
		for i in range(len(answers_list)):
		    objs[i].text = answers_list[i]
		    objs[i].question_id = qtm[i].question_id
		    objs[i].upc_id = id
		    objs[i].save()

		return
