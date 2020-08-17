from django.urls import reverse

from ..models import Attachment
from .base import BaseTestCase


class ViewTestCase(BaseTestCase):
    def setUp(self):
        super(ViewTestCase, self).setUp()
        self.item_url = reverse("testapp-detail", kwargs={"pk": self.obj.pk})

    def test_uploaded_attachment_urls_are_listed(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        response = self.client.get(self.item_url)
        attachment = Attachment.objects.attachments_for_object(self.obj)[0]
        self.assertTrue(attachment.attachment_file.url in str(response.content))

    def test_attachment_count_is_listed(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        self._upload_testfile()
        response = self.client.get(self.item_url)
        attachment_count = Attachment.objects.attachments_for_object(
            self.obj
        ).count()
        self.assertTrue(
            "Object has %d attachments" % attachment_count
            in str(response.content)
        )

    def test_upload_form_is_listed_with_add_permission(self):
        self.client.login(**self.cred_jon)
        response = self.client.get(self.item_url)
        self.assertTrue("<form" in str(response.content))

    def test_upload_form_is_not_listed_without_add_permission(self):
        self.jon.user_permissions.remove(self.add_permission)
        self.client.login(**self.cred_jon)
        response = self.client.get(self.item_url)
        self.assertFalse("<form" in str(response.content))

    def test_delete_link_is_listed_with_delete_permission(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        response = self.client.get(self.item_url)
        self.assertTrue("delete-attachment" in str(response.content))

    def test_delete_link_is_not_listed_without_delete_permission(self):
        self.jon.user_permissions.remove(self.del_permission)
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        response = self.client.get(self.item_url)
        self.assertFalse("delete-attachment" in str(response.content))

    def test_delete_link_is_listed_with_foreign_delete_permission(self):
        self.jon.user_permissions.add(self.del_foreign_permission)
        self.client.login(**self.cred_jane)
        self._upload_testfile()
        self.client.login(**self.cred_jon)
        response = self.client.get(self.item_url)
        self.assertTrue("delete-attachment" in str(response.content))

    def test_delete_link_is_not_listed_for_others_attachments(self):
        self.client.login(**self.cred_jane)
        self._upload_testfile()
        self.client.login(**self.cred_jon)
        response = self.client.get(self.item_url)
        self.assertFalse("delete-attachment" in str(response.content))
