from __future__ import unicode_literals

try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url

from .views import add_attachment, delete_attachment

app_name = "attachments"

urlpatterns = [
    url(
        r"^add-for/(?P<app_label>[\w\-]+)/(?P<model_name>[\w\-]+)/(?P<pk>\d+)/$",
        add_attachment,
        name="add",
    ),
    url(
        r"^add-for/(?P<app_label>[\w\-]+)/(?P<model_name>[\w\-]+)/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$",
        add_attachment,
        name="add",
    ),
    url(r"^delete/(?P<attachment_pk>\d+)/$", delete_attachment, name="delete"),
]
