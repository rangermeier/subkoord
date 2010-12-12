from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^event/', include('subkoord.event.urls')),
	(r'^user/', include('subkoord.users.urls')),
	(r'^wiki/', include('subkoord.wiki.urls')),
	(r'^newsletter/', include('subkoord.newsletter.urls')),
	(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'subkoord.event.views.event_cal', name="home"),
	url(r'^accounts/$',
		'django.contrib.auth.views.login', ),
	url(r'^accounts/login/$',
		'django.contrib.auth.views.login',
		name='login', ),
	url(r'^accounts/logout/$',
		'subkoord.users.views.logout_view',
		name='logout', ),
	url(r'^cron$',
		'subkoord.event.cron.reminder',
		name='cron', ),
	url(r'^backup$',
		'subkoord.event.cron.backup',
		name='backup', ),
)
