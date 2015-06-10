from django.conf.urls import patterns, include, url
from django.contrib import admin
from trips.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^login2/$',login),
	url(r'^home/$',home),
	url(r'^modify/$',modify),
	url(r'^register/$',register),
	url(r'^superuser/$',superuser),
)
