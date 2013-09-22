from django.conf.urls import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from filebrowser.sites import site
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^event/', include('event.urls')),
    (r'^user/', include('users.urls')),
    (r'^wiki/', include('wiki.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^newsletter/', include('newsletter.urls')),
    (r'^admin/filebrowser/', include(site.urls)),
    (r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
    url(r'^$', 'event.views.event_cal', name="home"),
    url(r'^accounts/$',
        'django.contrib.auth.views.login', ),
    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        name='login', ),
    url(r'^accounts/logout/$',
        'users.views.logout_view',
        name='logout', ),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
