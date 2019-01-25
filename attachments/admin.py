from __future__ import unicode_literals

from django.contrib.contenttypes.admin import GenericStackedInline

from .models import Attachment


class AttachmentInlines(GenericStackedInline):
    model = Attachment
    exclude = ()
    extra = 1
