from __future__ import unicode_literals

from attachments.models import Attachment
from django.contrib.contenttypes.admin import GenericStackedInline

class AttachmentInlines(GenericStackedInline):
    model = Attachment
    exclude = ()
    extra = 1
