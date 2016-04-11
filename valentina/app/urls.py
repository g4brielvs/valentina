from django.conf.urls import url
from valentina.app.views import (welcome, chat, profile, facebook, affiliation,
                                 report, logout)

urlpatterns = [
    url(r'^$', welcome, name='welcome'),
    url(r'^chat/(?P<hash_id>[\d\w]+)/$', chat, name='chat'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^facebook/$', facebook, name='facebook'),
    url(r'^join/$', affiliation, name='affiliation'),
    url(r'^report/$', report, name='report'),
    url(r'^logout/$', logout, name='logout'),
]
