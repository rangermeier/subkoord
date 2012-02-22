from django.conf.urls import *

urlpatterns = patterns('subkoord.users.views',
    url(r'^$', 'user_list', name="user_list"),
    url(r'^(?P<user_id>\d+)/$', 'user_view', name="user_view"),
    url(r'^password/$', 'user_change_password', name="user_change_password"),
)
