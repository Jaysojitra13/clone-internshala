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
	url(r'^applications/',views.ApplicationView.as_view(),name='applications'),
	url(r'^messages/',views.MessageView.as_view(),name='messages'),
	url(r'^savemsg/',views.SaveMsg.as_view(),name='save-messages'),
	url(r'^viewdetails/(?P<id>\d+)/$',views.ViewDetails.as_view(),name='view-details'),
	#re_path('link/(?P<type>\d+)$',views.ExistingPost.as_view(),name='existing-post'),
] 