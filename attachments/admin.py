from __future__ import unicode_literals

from django.contrib.contenttypes.admin import GenericTabularInline
from attachments.forms import AttachmentForm
from attachments.models import Attachment


class AttachmentInlines(GenericTabularInline):
    model = Attachment
    form = AttachmentForm
    exclude = ()
    extra = 1
