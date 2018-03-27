from django.contrib import admin
from django.urls import path, include, re_path
from .views import *
from django.conf.urls import url

app_name = 'company'
urlpatterns = [ 
	url(r'^contactdetail/',company_details.ContactDetailsView.as_view(), name='contact-detail'),
	url(r'^postdetail/',company_details.PostDetailsView.as_view(), name='post-detail'),
	url(r'^index/',company_details.Index.as_view(),name='index'),
	url(r'^existingpost/',post.ExistingPost.as_view(),name='existing-post'),
	url(r'^post/',post.PostView.as_view(),name='post'),
	url(r'^allpost/',post.AllPostView.as_view(),name='all-post'),
	url(r'^pastpost/',post.PastPostView.as_view(),name='past-post'),
	url(r'^applications/',applications.ApplicationView.as_view(),name='applications'),
	url(r'^accept/',message.MessageView.as_view(),name='messages'),
	url(r'^savemsg/',message.SaveMsg.as_view(),name='save-messages'),
	url(r'^viewdetails/(?P<id>\d+)/$',applications.ViewDetails.as_view(),name='view-details'),
	url(r'^reject/',applications.RejectView.as_view(),name='reject'),
	url(r'^confirm/',applications.ConfirmView.as_view(),name='confirm'),
	url(r'^confirmintern/(?P<pk>\d+)/$',applications.ConfirmInternView.as_view(),name='confirm-intern'),
	url(r'^rejectintern/(?P<pk>\d+)/$',applications.RejectInternView.as_view(),name='reject-intern'),
	url(r'^listintern/',applications.ListofInternView.as_view(),name='list-intern'),
	url(r'^test/',test_module.GenerateQuestionView.as_view(),name='test'),
	url(r'^listofquestion/(?P<type>\w+)/$',test_module.ListofQuestionView.as_view(),name='listofquestion'),
	url(r'^generatetest/(?P<id>\d+)/$',test_module.GenerateTestView.as_view(),name='generate-test'),
	url(r'^createtest/',test_module.CreateTestView.as_view(),name='create-test'),
	url(r'^result/(?P<id>\d+)/$',test_module.ResultView.as_view(), name='result'),
	url(r'^checkanswer/',test_module.CheckAnswerView.as_view(), name='check-answer'),
	url(r'^countresult/',test_module.CountResultView.as_view(), name='count-result'),
	url(r'^deletesinglequestion/',test_module.DeleteOneQuestionView.as_view(), name='delete-singlequestion'),
	url(r'^deleteallquesitons/',test_module.DeleteAllQuestionView.as_view(), name='delete-allquestion'),

	

	#re_path('link/(?P<type>\d+)$',views.ExistingPost.as_view(),name='existing-post'),
] 