from django.conf.urls.defaults import *

urlpatterns = patterns('subkoord.event.views',
    url(r'^$', 'event_cal', name="event_index"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'event_cal', name="event_cal"),
    url(r'^(?P<event_id>\d+)/$', 'event', name="event"),
    url(r'^(?P<event_id>\d+)/edit/$', 'event_edit', name="event_edit"),
    url(r'^(?P<event_id>\d+)/delete/$', 'event_delete', name="event_delete"),
    url(r'^new/$', 'event_new', name="event_new"),
    url(r'^archive/$', 'event_index', {'archive': True}, name="event_archive", ),
    url(r'^(?P<event_id>\d+)/task/(?P<task_id>\d+)/$', 'job_add', name="job_add"),
    url(r'^(?P<event_id>\d+)/job/(?P<job_id>\d+)/delete$', 'job_delete', name="job_delete"),
    url(r'^(?P<event_id>\d+)/note$', 'note_add', name="note_add"),
)
