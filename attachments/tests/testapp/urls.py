from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^attachments/', include('attachments.urls', namespace='attachments')),
    url(r'^admin/', include(admin.site.urls)),
]
