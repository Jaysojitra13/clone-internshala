from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf.urls import url

app_name = 'company'
urlpatterns = [ 
	url(r'^contactdetail/',views.ContactDetailsView.as_view(), name='contact-detail'),
	url(r'^postdetail/',views.PostDetailsView.as_view(), name='post-detail'),
	url(r'^index/',views.Index.as_view(),name='index'),
	url(r'^existingpost/',views.ExistingPost.as_view(),name='existing-post'),
	url(r'^post/',views.PostView.as_view(),name='post'),
	url(r'^allpost/',views.AllPostView.as_view(),name='all-post'),
	url(r'^pastpost/',views.PastPostView.as_view(),name='past-post'),
	url(r'^applications/',views.ApplicationView.as_view(),name='applications'),
	url(r'^accept/',views.MessageView.as_view(),name='messages'),
	url(r'^savemsg/',views.SaveMsg.as_view(),name='save-messages'),
	url(r'^viewdetails/(?P<id>\d+)/$',views.ViewDetails.as_view(),name='view-details'),
	url(r'^reject/',views.RejectView.as_view(),name='reject'),
	url(r'^confirm/',views.ConfirmView.as_view(),name='confirm'),
	url(r'^confirmintern/(?P<pk>\d+)/$',views.ConfirmInternView.as_view(),name='confirm-intern'),
	url(r'^rejectintern/(?P<pk>\d+)/$',views.RejectInternView.as_view(),name='reject-intern'),
	url(r'^listintern/',views.ListofInternView.as_view(),name='list-intern'),
	url(r'^test/',views.GenerateQuestionView.as_view(),name='test'),
	url(r'^listofquestion/(?P<type>\w+)/$',views.ListofQuestionView.as_view(),name='listofquestion'),
	url(r'^generatetest/(?P<id>\d+)/$',views.GenerateTestView.as_view(),name='generate-test'),
	url(r'^createtest/',views.CreateTestView.as_view(),name='create-test'),
	url(r'^result/(?P<id>\d+)/$',views.ResultView.as_view(), name='result'),
	url(r'^checkanswer/',views.CheckAnswerView.as_view(), name='check-answer'),
	url(r'^countresult/',views.CountResultView.as_view(), name='count-result'),
	url(r'^deletesinglequestion/',views.DeleteOneQuestionView.as_view(), name='delete-singlequestion'),
	url(r'^deleteallquesitons/',views.DeleteAllQuestionView.as_view(), name='delete-allquestion'),

	

	#re_path('link/(?P<type>\d+)$',views.ExistingPost.as_view(),name='existing-post'),
] 