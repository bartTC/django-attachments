from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AttachmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = "attachments"
    verbose_name = _("Attachments")
