from django.conf.urls import url
from valentina.app.views import welcome, blocked, female_only

urlpatterns = [
    url(r'^$', welcome, name='welcome'),
    url(r'^blocked/$', blocked, name='blocked'),
    url(r'^oops/$', female_only, name='female_only'),
]
