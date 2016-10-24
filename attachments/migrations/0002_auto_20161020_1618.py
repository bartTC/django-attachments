# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import attachments.models


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attachment',
            options={'ordering': ['-created'], 'verbose_name': '\u0444\u0430\u0439\u043b', 'verbose_name_plural': '\u0444\u0430\u0439\u043b\u044b', 'permissions': (('delete_foreign_attachments', 'Can delete foreign attachments'),)},
        ),
        migrations.AddField(
            model_name='attachment',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='\u0414\u043e\u0441\u0442\u0443\u043f\u0435\u043d \u043a\u043b\u0438\u0435\u043d\u0442\u0443'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='name',
            field=models.CharField(max_length=1024, null=True, verbose_name='\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='attachment_file',
            field=models.FileField(upload_to=attachments.models.attachment_upload, max_length=1024, verbose_name='attachment'),
        ),
    ]
