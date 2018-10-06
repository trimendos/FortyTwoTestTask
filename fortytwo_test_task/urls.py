from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url
from django.contrib.flatpages.views import flatpage
from django.contrib import admin

from apps.hello.views import MainPageView, RequestsPageView


admin.autodiscover()
urlpatterns = patterns(
    '',
    url('^$', MainPageView.as_view(), name='main_page'),
    url(r'^requests_page/$', RequestsPageView.as_view(), name='requests_page'),
    url(r'^admin/', include(admin.site.urls)),
    url(r"^update_profile_page/$",
        login_required(flatpage),
        {'url': "/update_profile_page/"},
        name="update_profile_page"),
    url(r"^accounts/", include("django.contrib.auth.urls",
                               namespace="accounts")),
)
urlpatterns += staticfiles_urlpatterns()
