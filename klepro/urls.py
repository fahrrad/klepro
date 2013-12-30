from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

from producten.views import ProductenListView, NaTeKijkenProductenListView

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'klepro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(
        regex=r'^producten/$',
        view=ProductenListView.as_view(),
        name="list"
    ),
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    url(
        regex='^$',
        view=RedirectView.as_view(url='/producten'),
        name='start',
    ),
    url(
        regex='^favicon.ico$',
        view=RedirectView.as_view(url='/static/favicon.ico'),
        name='favicon'
    ),
    url(
        regex='^producten_checken/$',
        view=NaTeKijkenProductenListView.as_view(),
        name='na_te_kijken'

    )
)
