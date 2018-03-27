from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import Internship, SignIn_SignUp, intern_details

app_name = 'intern'
urlpatterns = [ 
	#re_path('',views.Home.as_view(), name='home'),
	url(r'^index/',intern_details.HomeView.as_view(), name='index'),
	url(r'^personaldetail/',intern_details.PersonalDetailView.as_view(), name='personal-detail'),
	url(r'^updatepersonaldetail/(?P<pk>\d*)',intern_details.UpdatePersonalDetailView.as_view(), name='updatepersonal-detail'),
	          
	url(r'^academicdetail/',intern_details.AcademicDetailView.as_view(), name='academic-detail'),
	url(r'^updateacademicdetail/(?P<pk>\d*)',intern_details.UpdateAcademicDetailView.as_view(), name='updateacademic-detail'),
	
	url(r'^projectdetail/',intern_details.ProjectDetailView.as_view(), name='project-detail'),
	url(r'^internship/',Internship.InternshipDetailView.as_view(), name='internship-detail'),
	url(r'^internpost/(?P<company_id>\d+)/(?P<post_id>\d+)/$', Internship.InternPostConnection.as_view(), name='internpost-connection'),
	url(r'^readmessages/(?P<id>\d+)/$',Internship.ReadMessages, name='read-messages'),
	#re_path(r'^applied/(?P<type>\w+)/$',views.AppliedInternship.as_view(), name='applied-internship'),
	
	#re_path('detail/(?P<pk>[\-\w]+)/$',views.detail_profile, name='account-detail'),
] 

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, e=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)