from __future__ import unicode_literals

from django import forms
from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _

from .models import Attachment

config = apps.get_app_config("attachments")


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


def custom_attachment_validators(uploaded_file):
    for validator in getattr(config, "attachment_validators", ()):
        validator(uploaded_file)


class AttachmentForm(forms.ModelForm):
    attachment_file = forms.FileField(
        label=_("Upload attachment"),
        validators=[validate_max_size, custom_attachment_validators]
    )

    class Meta:
        model = Attachment
        fields = ("attachment_file",)

    def save(self, request, obj, *args, **kwargs):
        self.instance.creator = request.user
        self.instance.content_type = ContentType.objects.get_for_model(obj)
        self.instance.object_id = obj.pk
        super(AttachmentForm, self).save(*args, **kwargs)
