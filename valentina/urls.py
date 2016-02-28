"""valentina URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from valentina.home.views import home, blocked, female_only

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^oauth/', include('social.apps.django_app.urls', namespace='oauth')),
    url(r'^app/', include('valentina.app.urls', namespace='app')),
    url(r'^blocked/$', blocked, name='blocked'),
    url(r'^exclusive/$', female_only, name='female_only'),
    url(r'^admin/', admin.site.urls),
]
