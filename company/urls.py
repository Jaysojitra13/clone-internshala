from django.contrib import admin
from django.urls import path, include, re_path
from . import views

app_name = 'company'
urlpatterns = [
	re_path('contactdetail/',views.ContactDetailsView.as_view(), name='contact-detail'),
	re_path('postdetail/',views.PostDetailsView.as_view(), name='post-detail'),
	re_path('index/',views.Index.as_view(),name='index'),
	re_path('existingpost/',views.ExistingPost.as_view(),name='existing-post'),
	re_path('applications/',views.ApplicationView.as_view(),name='applications'),
	re_path('messages/',views.MessageView.as_view(),name='messages'),
	re_path('savemsg/',views.SaveMsg.as_view(),name='save-messages'),
	#re_path('link/(?P<type>\d+)$',views.ExistingPost.as_view(),name='existing-post'),
]