# coding=utf-8
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from attachments.models import Attachment


class AttachmentForm(forms.ModelForm):
    attachment_file = forms.FileField(label='Файл')

    class Meta:
        model = Attachment
        fields = ('attachment_file', 'name', 'is_public',)
