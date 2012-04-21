from django.conf.urls import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from filebrowser.sites import site
from django.contrib import admin
from tastypie.api import Api
from subkoord.event.api import *
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(EventResource())
#v1_api.register(TaskResource())
#v1_api.register(JobResource())

urlpatterns = patterns('',
    (r'^event/', include('subkoord.event.urls')),
    (r'^user/', include('subkoord.users.urls')),
    (r'^wiki/', include('subkoord.wiki.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^newsletter/', include('subkoord.newsletter.urls')),
    (r'^admin/filebrowser/', include(site.urls)),
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),
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
