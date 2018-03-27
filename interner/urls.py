"""interner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
# from intern import views
from company import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from intern.views import  SignIn_SignUp, intern_details
 
urlpatterns = [
    url(r'^checkuser/(?P<type>\w+)/$', SignIn_SignUp.CheckUser, name='check-user'),
    url(r'^checklogin/(?P<type>\w+)/$', SignIn_SignUp.CheckLogin, name='check-login'),
    url(r'^accounts/signup/$', SignIn_SignUp.MySignUpView.as_view(), name='check-signupuser'),
    url(r'^accounts/login/$', SignIn_SignUp.MyLogInView.as_view(), name='check-loginuser'),
    url(r'^admin/', admin.site.urls),
    url(r'^intern/', include('intern.urls')),
    url(r'^company/', include('company.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', intern_details.Home.as_view(), name='home'),
    


] 
 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
