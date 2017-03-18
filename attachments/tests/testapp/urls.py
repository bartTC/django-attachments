from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import DetailView

from .models import TestModel

admin.autodiscover()

urlpatterns = [
    url(r'^attachments/', include('attachments.urls', namespace='attachments')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^testapp/(?P<pk>\d+)/$', DetailView.as_view(
        template_name='testmodel_detail.html',
        queryset=TestModel.objects.all()
    ), name='testapp-detail')
]
