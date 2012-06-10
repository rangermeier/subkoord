from django.conf.urls import *

urlpatterns = patterns('wiki.views',
    url(r'^$', 'index', name="wiki_index"),
    url(r'^new/$', 'edit', name="wiki_new"),
    url(r'^(?P<title>[A-Za-z0-9\-_\.]{2,})/$', 'page', name="wiki_page"),
    url(r'^(?P<title>[A-Za-z0-9\-_\.]{2,})/edit/$', 'edit', name="wiki_edit"),
    url(r'^(?P<title>[A-Za-z0-9\-_\.]{2,})/delete/$', 'delete', name="wiki_delete"),
)
