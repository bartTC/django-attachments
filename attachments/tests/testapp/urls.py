try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url

from django.conf.urls import include
from django.contrib import admin
from django.views.generic import DetailView

from .models import TestModel

admin.autodiscover()

urlpatterns = [
    url(r"^attachments/", include("attachments.urls", namespace="attachments")),
    url(r"^admin/", admin.site.urls),
    url(
        r"^testapp/(?P<pk>\d+)/$",
        DetailView.as_view(
            template_name="testmodel_detail.html",
            queryset=TestModel.objects.all(),
        ),
        name="testapp-detail",
    ),
]
