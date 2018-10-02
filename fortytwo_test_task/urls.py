from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url

from django.contrib import admin

from apps.hello.views import MainPageView


admin.autodiscover()
urlpatterns = patterns(
    '',
    url('^$', MainPageView.as_view(), name='main_page'),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns(
    'django.contrib.flatpages.views',
    url(r'^requests_page/$',
        'flatpage', {'url': '/requests_page/'},
        name='requests_page'),
)
