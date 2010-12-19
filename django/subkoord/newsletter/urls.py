from django.conf.urls.defaults import *

urlpatterns = patterns('subkoord.newsletter.views',
	url(r'^$', 'index', name="newsletter_index"),
	url(r'^compose/$', 'message_new', name="message_new"),
	url(r'^message/(?P<message_id>\d+)/$', 'message', name="message"),
	url(r'^message/archive/$', 'message_archive', name="message_archive"),
	url(r'^job/(?P<job_id>\d+)/$', 'job', name="job"),
	url(r'^send/$', 'job_new', name="job_new"),
	url(r'^subscriber/(?P<subscriber_id>\d+)/$', 'subscriber', name="subscriber"),
	url(r'^subscriber/(?P<subscriber_id>\d+)/delete/$', 'subscriber_delete', name="subscriber_delete"),
	url(r'^confirm/(?P<subscriber_id>\d+)/(?P<token>\w{12})$', 'subscriber_confirm', name="subscriber_confirm"),
	url(r'^delete/(?P<subscriber_id>\d+)/(?P<token>\w{12})$', 'subscriber_public_delete', name="subscriber_public_delete"),
	url(r'^mailinglist/(?P<list_id>\d+)/add/$', 'subscribers_add', name="subscribers_add"),
	url(r'^mailinglist/(?P<list_id>\d+)/subscribe/$', 'subscriber_add', name="subscriber_add"),
	url(r'^mailinglist/(?P<list_id>\d+)/$', 'subscribers_list', name="subscribers_list"),
)
