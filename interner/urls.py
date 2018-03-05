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
from intern import views
from company import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    url(r'^checkuser/(?P<type>\w+)/$', views.CheckUser, name='check-user'),
    url(r'^checklogin/(?P<type>\w+)/$', views.CheckLogin, name='check-login'),
    url(r'^accounts/signup/$', views.MySignUpView.as_view(), name='check-signupuser'),
     url(r'^accounts/login/$', views.MyLogInView.as_view(), name='check-loginuser'),
    path('admin/', admin.site.urls),
    path('intern/', include('intern.urls')),
    path('company/', include('company.urls')),
    re_path(r'^accounts/', include('allauth.urls')),
    path('', views.Home.as_view(), name='home'),
    


] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
