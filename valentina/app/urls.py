from django.conf.urls import url
from valentina.app.views import welcome, logout

urlpatterns = [
    url(r'^$', welcome, name='welcome'),
    url(r'^logout/$', logout, name='logout'),
]
