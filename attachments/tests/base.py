# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from ..models import Attachment
from .testapp.models import TestModel


class BaseTestCase(TestCase):
    def setUp(self):
        """
        Create two users with `attachments.add_attachment` permission
        and one object to attach files to.
        """
        content_type = ContentType.objects.get_for_model(Attachment)
        self.add_permission = Permission.objects.get(
            content_type=content_type, codename="add_attachment"
        )
        self.del_permission = Permission.objects.get(
            content_type=content_type, codename="delete_attachment"
        )

        self.del_foreign_permission = Permission.objects.get(
            content_type=content_type, codename="delete_foreign_attachments"
        )

        self.cred_jon = {"username": "jon", "password": "foobar"}
        self.cred_jane = {"username": "jane", "password": "foobar"}
        self.jon = User.objects.create_user(**self.cred_jon)
        self.jon.user_permissions.add(self.add_permission)
        self.jon.user_permissions.add(self.del_permission)

        self.jane = User.objects.create_user(**self.cred_jane)
        self.jane.user_permissions.add(self.add_permission)
        self.jane.user_permissions.add(self.del_permission)

        self.obj = TestModel.objects.create(title="My first test item")

    def _upload_testfile(self, file_obj=None):
        """
        Uploads a sample file for the given user.
        """
        add_url = reverse(
            "attachments:add",
            kwargs={
                "app_label": "testapp",
                "model_name": "testmodel",
                "pk": self.obj.pk,
            },
        )

        if not file_obj:
            file_obj = SimpleUploadedFile(
                "Ünicode Filename 🙂.jpg",
                b"file content",
                content_type="image/jpeg",
            )
        return self.client.post(
            add_url, {"attachment_file": file_obj}, follow=True
        )
