from django.conf.urls import patterns, include, url

from django.contrib import admin

from producten.views import ProductDetailView
from producten.views import ProductenListView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'klepro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(
        regex=r"^producten/(?P<pk>\d+)/$",
        view=ProductDetailView.as_view(),
        name="detail"
    ),
    url(
        regex=r'^producten/$',
        view=ProductenListView.as_view(),
        name="list"
    ),
)
