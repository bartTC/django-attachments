from django.conf.urls import *
from .views import add_attachment, delete_attachment

urlpatterns = patterns('',
    url(r'^add-for/(?P<app_label>[\w\-]+)/(?P<model_name>[\w\-]+)/(?P<pk>\d+)/$',
        add_attachment, name="add"),
    url(r'^delete/(?P<attachment_pk>\d+)/$',
        delete_attachment, name="delete"),
)
