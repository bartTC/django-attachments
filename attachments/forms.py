from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _

from .models import Attachment


def validate_max_size(data):
    if (
        hasattr(settings, "FILE_UPLOAD_MAX_SIZE")
        and data.size > settings.FILE_UPLOAD_MAX_SIZE
    ):
        raise forms.ValidationError(
            _("File exceeds maximum size of {size}").format(
                size=filesizeformat(settings.FILE_UPLOAD_MAX_SIZE)
            )
        )


class AttachmentForm(forms.ModelForm):
    attachment_file = forms.FileField(
        label=_("Upload attachment"), validators=[validate_max_size]
    )

    class Meta:
        model = Attachment
        fields = ("attachment_file",)

    def save(self, request, obj, *args, **kwargs):
        self.instance.creator = request.user
        self.instance.content_type = ContentType.objects.get_for_model(obj)
        self.instance.object_id = obj.pk
        super(AttachmentForm, self).save(*args, **kwargs)
