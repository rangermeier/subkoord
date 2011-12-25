from django.conf.urls.defaults import *

urlpatterns = patterns('subkoord.newsletter.views',
    url(r'^$', 'index', name="newsletter_index"),
    url(r'^compose/$', 'message_new', name="message_new"),
    url(r'^message/(?P<message_id>\d+)/$', 'message', name="message"),
    url(r'^message/(?P<message_id>\d+)/preview/$', 'job_new', {'preview_send': True},  name="message_preview"),
    url(r'^message/archive/$', 'message_archive', name="message_archive"),
    url(r'^job/(?P<job_id>\d+)/$', 'job', name="job"),
    url(r'^send/$', 'job_new', name="job_new"),
    url(r'^subscriber/(?P<subscriber_id>\d+)/$', 'subscriber', name="subscriber"),
    url(r'^subscriber/(?P<subscriber_id>\d+)/delete/$', 'subscriber_delete', name="subscriber_delete"),
    url(r'^subscriber/(?P<subscribers_ids>[0-9\,]+)/delete/$', 'subscribers_delete', name="subscribers_delete"),
    url(r'^confirm/(?P<subscriber_id>\d+)/(?P<token>\w{12})$', 'subscriber_confirm', name="subscriber_confirm"),
    url(r'^delete/(?P<subscriber_id>\d+)/(?P<token>\w{12})$', 'subscriber_public_delete', name="subscriber_public_delete"),
    url(r'^mailinglist/(?P<list_id>\d+)/add/$', 'subscribers_add', name="subscribers_add"),
    url(r'^mailinglist/(?P<list_id>\d+)/subscribe/$', 'subscriber_add', name="subscriber_add"),
    url(r'^mailinglist/(?P<list_id>\d+)/$', 'subscribers_list', name="subscribers_list"),
    url(r'^errors/$', 'error_mailbox', name="error_mailbox"),
    url(r'^errors/empty/$', 'empty_error_mailbox', name="empty_error_mailbox"),
    url(r'^errors/(?P<msg_id>\d+)/delete$', 'delete_error_mail', name="delete_error_mail"),
    url(r'^errors/unassigned/delete$', 'delete_unassigned_mails', name="delete_unassigned_mails"),
)
