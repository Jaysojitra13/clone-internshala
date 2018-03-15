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
	url(r'^test/',views.AddQuestionView,name='test'),


	#re_path('link/(?P<type>\d+)$',views.ExistingPost.as_view(),name='existing-post'),
] 