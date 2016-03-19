from __future__ import unicode_literals

from django.conf.urls import url
from .views import add_attachment, delete_attachment

urlpatterns = [
    url(r'^add-for/(?P<app_label>[\w\-]+)/(?P<model_name>[\w\-]+)/(?P<pk>\d+)/$',
        add_attachment, name="add"),
    url(r'^delete/(?P<attachment_pk>\d+)/$',
        delete_attachment, name="delete"),
]
