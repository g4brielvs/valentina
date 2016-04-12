from django.conf.urls import url
from valentina.app.views import (welcome, chat, profile, facebook, report,
                                 create_affiliation, list_affiliations,
                                 chat_preferences, logout)

urlpatterns = [
    url(r'^$', welcome, name='welcome'),
    url(r'^chat/preferences/$', chat_preferences, name='preferences'),
    url(r'^chat/(?P<hash_id>[\d\w]+)/$', chat, name='chat'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^facebook/$', facebook, name='facebook'),
    url(r'^join/$', create_affiliation, name='affiliation'),
    url(r'^chats/$', list_affiliations, name='affiliations'),
    url(r'^report/$', report, name='report'),
    url(r'^logout/$', logout, name='logout'),
]
