from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'intern'
urlpatterns = [ 
	#re_path('',views.Home.as_view(), name='home'),
	url(r'^index/',views.HomeView.as_view(), name='index'),
	url(r'^personaldetail/',views.PersonalDetailView.as_view(), name='personal-detail'),
	url(r'^updatepersonaldetail/(?P<pk>\d*)',views.UpdatePersonalDetailView.as_view(), name='updatepersonal-detail'),
	          
	url(r'^academicdetail/',views.AcademicDetailView.as_view(), name='academic-detail'),
	url(r'^updateacademicdetail/(?P<pk>\d*)',views.UpdateAcademicDetailView.as_view(), name='updateacademic-detail'),
	
	url(r'^projectdetail/',views.ProjectDetailView.as_view(), name='project-detail'),
	url(r'^internship/',views.InternshipDetailView.as_view(), name='internship-detail'),
	url(r'^internpost/(?P<company_id>\d+)/(?P<post_id>\d+)/$', views.InternPostConnection.as_view(), name='internpost-connection'),
	url(r'^readmessages/(?P<id>\d+)/$',views.ReadMessages, name='read-messages'),
	#re_path(r'^applied/(?P<type>\w+)/$',views.AppliedInternship.as_view(), name='applied-internship'),
	
	#re_path('detail/(?P<pk>[\-\w]+)/$',views.detail_profile, name='account-detail'),
] 

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)