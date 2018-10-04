from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url

from django.contrib import admin

from apps.hello.views import MainPageView, RequestsPageView


admin.autodiscover()
urlpatterns = patterns(
    '',
    url('^$', MainPageView.as_view(), name='main_page'),
    url(r'^requests_page/$', RequestsPageView.as_view(), name='requests_page'),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
