from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^event/', include('subkoord.event.urls')),
	(r'^user/', include('subkoord.users.urls')),
	(r'^wiki/', include('subkoord.wiki.urls')),
	(r'^grappelli/', include('grappelli.urls')),
	(r'^newsletter/', include('subkoord.newsletter.urls')),
	(r'^admin/filebrowser/', include('filebrowser.urls')),
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
)

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
