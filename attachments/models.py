# coding=utf-8
from __future__ import unicode_literals

import os

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _


def attachment_upload(instance, filename):
    """Stores the attachment in a "per module/appname/primary key" folder"""
    return 'attachments/{app}_{model}/{pk}/{filename}'.format(
        app=instance.content_object._meta.app_label,
        model=instance.content_object._meta.object_name.lower(),
        pk=instance.content_object.pk,
        filename=filename)


class AttachmentManager(models.Manager):
    def attachments_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id,
                           object_id=obj.pk)


class Attachment(models.Model):
    objects = AttachmentManager()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="created_attachments",
        verbose_name=_('creator'))
    name = models.CharField(verbose_name='описание',
                            null=True, blank=True, max_length=1024)
    attachment_file = models.FileField(
        _('attachment'), upload_to=attachment_upload, max_length=1024)
    is_public = models.BooleanField('Доступен клиенту', default=False)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = u'файл'
        verbose_name_plural = u'файлы'
        ordering = ['-created']
        permissions = (
            ('delete_foreign_attachments', _('Can delete foreign attachments')),
        )

    def __unicode__(self):
        return '{} attached {}'.format(
            self.creator.get_username(),
            self.attachment_file.name)

    @property
    def filename(self):
        return os.path.split(self.attachment_file.name)[1]
