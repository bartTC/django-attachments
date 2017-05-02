# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forwards(apps, schema_editor):
    group_model = apps.get_model('auth', 'Group')
    permission_model = apps.get_model('auth', 'Permission')
    group = group_model.objects.get(id=1)
    permissions = permission_model.objects.filter(
        content_type__app_label='attachments')
    group.permissions.add(*permissions)


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0002_auto_20161020_1618'),
    ]

    operations = [
        migrations.RunPython(forwards)
    ]
