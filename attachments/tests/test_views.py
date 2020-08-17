import os

import mock
from django.urls import reverse

from ..models import Attachment
from .base import BaseTestCase


class ViewTestCase(BaseTestCase):
    def test_empty_post_to_form_wont_create_attachment(self):
        add_url = reverse(
            "attachments:add",
            kwargs={
                "app_label": "testapp",
                "model_name": "testmodel",
                "pk": self.obj.pk,
            },
        )
        response = self.client.post(add_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(Attachment.objects.count(), 0)
        self.assertEqual(
            Attachment.objects.attachments_for_object(self.obj).count(), 0
        )

    def test_invalid_model_wont_fail(self):
        add_url = reverse(
            "attachments:add",
            kwargs={
                "app_label": "thisdoes",
                "model_name": "notexist",
                "pk": self.obj.pk,
            },
        )
        response = self.client.post(add_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(Attachment.objects.count(), 0)
        self.assertEqual(
            Attachment.objects.attachments_for_object(self.obj).count(), 0
        )

    def test_invalid_attachment_wont_fail(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile(file_obj="Not a UploadedFile object")
        self.assertEqual(Attachment.objects.count(), 0)
        self.assertEqual(
            Attachment.objects.attachments_for_object(self.obj).count(), 0
        )

    def test_upload_size_less_than_limit(self):
        # NOTE: in all of the other tests there's no limit specified
        # so they will cover the branch where the setting is missing
        with self.settings(FILE_UPLOAD_MAX_SIZE=1024):
            self.client.login(**self.cred_jon)
            self._upload_testfile()
            self.assertEqual(Attachment.objects.count(), 1)
            self.assertEqual(
                Attachment.objects.attachments_for_object(self.obj).count(), 1
            )

    def test_upload_size_more_than_limit(self):
        # we set a limit of 1 byte b/c the file used for testing
        # is very small
        with self.settings(FILE_UPLOAD_MAX_SIZE=1):
            self.client.login(**self.cred_jon)
            self._upload_testfile()
            self.assertEqual(Attachment.objects.count(), 0)
            self.assertEqual(
                Attachment.objects.attachments_for_object(self.obj).count(), 0
            )

    def test_upload_without_permission(self):
        """
        Remove the 'add permission' and try to upload a file.
        """
        self.jon.user_permissions.remove(self.add_permission)

        self.client.login(**self.cred_jon)
        self._upload_testfile()
        self.assertEqual(Attachment.objects.count(), 0)
        self.assertEqual(
            Attachment.objects.attachments_for_object(self.obj).count(), 0
        )

    def test_upload_with_permission(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        self.assertEqual(Attachment.objects.count(), 1)
        self.assertEqual(
            Attachment.objects.attachments_for_object(self.obj).count(), 1
        )

    def test_unauthed_user_cant_delete_attachment(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        att = Attachment.objects.first()
        del_url = reverse(
            "attachments:delete", kwargs={"attachment_pk": att.pk}
        )
        self.client.logout()
        self.client.get(del_url, follow=True)
        self.assertEqual(Attachment.objects.count(), 1)
        self.assertEqual(
            Attachment.objects.attachments_for_object(self.obj).count(), 1
        )

    def test_author_can_delete_attachment(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        att = Attachment.objects.first()
        file_path = att.attachment_file.path
        del_url = reverse(
            "attachments:delete", kwargs={"attachment_pk": att.pk}
        )
        self.client.get(del_url, follow=True)
        self.assertEqual(Attachment.objects.count(), 0)
        # file on disk is still present b/c setting not specified
        self.assertTrue(os.path.exists(file_path))

    def test_author_cant_delete_attachment_if_no_delete_permission(self):
        self.jon.user_permissions.remove(self.del_permission)

        self.client.login(**self.cred_jon)
        self._upload_testfile()
        att = Attachment.objects.first()
        del_url = reverse(
            "attachments:delete", kwargs={"attachment_pk": att.pk}
        )
        self.client.get(del_url, follow=True)
        self.assertEqual(Attachment.objects.count(), 1)

    def test_author_cant_delete_others_attachment(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        obj1 = Attachment.objects.order_by("-created")[0]

        self.client.login(**self.cred_jane)
        self._upload_testfile()
        obj2 = Attachment.objects.order_by("-created")[0]

        self.assertNotEqual(obj1, obj2)

        # Jon can't delete Janes attachment
        self.client.login(**self.cred_jon)
        del_url = reverse(
            "attachments:delete", kwargs={"attachment_pk": obj2.pk}
        )
        self.client.get(del_url, follow=True)

        self.assertEqual(Attachment.objects.count(), 2)

    def test_author_can_delete_others_attachment_with_permission(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        obj1 = Attachment.objects.order_by("-created")[0]
        path1 = obj1.attachment_file.path

        self.client.login(**self.cred_jane)
        self._upload_testfile()
        obj2 = Attachment.objects.order_by("-created")[0]
        path2 = obj2.attachment_file.path

        self.assertNotEqual(obj1, obj2)

        # Jon has the `delete_foreign_attachments` permission so he can
        # delete Janes attachment
        self.jon.user_permissions.add(self.del_foreign_permission)
        self.client.login(**self.cred_jon)

        # explicitly set the delete setting to False to
        # cover that branch as well
        with self.settings(DELETE_ATTACHMENT_FILE=False):
            del_url = reverse(
                "attachments:delete", kwargs={"attachment_pk": obj2.pk}
            )
            self.client.get(del_url, follow=True)

            self.assertEqual(Attachment.objects.count(), 1)
            self.assertTrue(os.path.exists(path1))
            self.assertTrue(os.path.exists(path2))

    def test_delete_removes_files_from_disk_if_settings(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        att = Attachment.objects.first()
        file_path = att.attachment_file.path
        with self.settings(DELETE_ATTACHMENTS_FROM_DISK=True):
            del_url = reverse(
                "attachments:delete", kwargs={"attachment_pk": att.pk}
            )
            self.client.get(del_url, follow=True)
            self.assertEqual(Attachment.objects.count(), 0)
            self.assertFalse(os.path.exists(file_path))

    def test_delete_does_not_raise_if_settings_and_file_missing(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        att = Attachment.objects.first()
        file_path = att.attachment_file.path
        # remove the file before hand
        os.remove(file_path)
        with self.settings(DELETE_ATTACHMENTS_FROM_DISK=True):
            del_url = reverse(
                "attachments:delete", kwargs={"attachment_pk": att.pk}
            )
            self.client.get(del_url, follow=True)
            self.assertEqual(Attachment.objects.count(), 0)
            self.assertFalse(os.path.exists(file_path))

    def test_delete_does_not_raise_if_os_remove_raises(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        att = Attachment.objects.first()

        with mock.patch("attachments.views.os.remove") as _mock:
            _mock.side_effect = OSError("Test file does not exist")
            with self.settings(DELETE_ATTACHMENTS_FROM_DISK=True):
                del_url = reverse(
                    "attachments:delete", kwargs={"attachment_pk": att.pk}
                )
                self.client.get(del_url, follow=True)
                self.assertEqual(Attachment.objects.count(), 0)
                # NOTE: we don't assert the file path here because
                # the mock which raises will not actually delete it
