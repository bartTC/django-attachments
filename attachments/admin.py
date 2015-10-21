from attachments.models import Attachment
from django.contrib.contenttypes.admin import GenericStackedInline

class AttachmentInlines(GenericStackedInline):
    model = Attachment
    extra = 1