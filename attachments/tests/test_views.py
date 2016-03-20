from __future__ import unicode_literals

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from attachments.models import Attachment

from .base import BaseTestCase


class ViewTestCase(BaseTestCase):
    def test_empty_post_to_form_wont_create_attachment(self):
        add_url = reverse('attachments:add', kwargs={
            'app_label': 'testapp',
            'model_name': 'testmodel',
            'pk': self.obj.pk,
        })
        response = self.client.post(add_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(Attachment.objects.count(), 0)
        self.assertEqual(Attachment.objects.attachments_for_object(self.obj).count(), 0)

    def test_invalid_model_wont_fail(self):
        add_url = reverse('attachments:add', kwargs={
            'app_label': 'thisdoes',
            'model_name': 'notexist',
            'pk': self.obj.pk,
        })
        response = self.client.post(add_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(Attachment.objects.count(), 0)
        self.assertEqual(Attachment.objects.attachments_for_object(self.obj).count(), 0)

    def test_invalid_attachment_wont_fail(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile(file_obj='Not a UploadedFile object')
        self.assertEqual(Attachment.objects.count(), 0)
        self.assertEqual(Attachment.objects.attachments_for_object(self.obj).count(), 0)

    def test_upload_without_permission(self):
        """
        Remove the 'add permission' and try to upload a file.
        """
        self.jon.user_permissions.remove(self.add_permission)

        self.client.login(**self.cred_jon)
        self._upload_testfile()
        self.assertEqual(Attachment.objects.count(), 0)
        self.assertEqual(Attachment.objects.attachments_for_object(self.obj).count(), 0)

    def test_upload_with_permission(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        self.assertEqual(Attachment.objects.count(), 1)
        self.assertEqual(Attachment.objects.attachments_for_object(self.obj).count(), 1)

    def test_unauthed_user_cant_delete_attachment(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        att = Attachment.objects.first()
        del_url = reverse('attachments:delete',
                          kwargs={'attachment_pk': att.pk,})
        self.client.logout()
        self.client.get(del_url, follow=True)
        self.assertEqual(Attachment.objects.count(), 1)
        self.assertEqual(
            Attachment.objects.attachments_for_object(self.obj).count(), 1)

    def test_author_can_delete_attachment(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        att = Attachment.objects.first()
        del_url = reverse('attachments:delete', kwargs={'attachment_pk': att.pk,})
        self.client.get(del_url, follow=True)
        self.assertEqual(Attachment.objects.count(), 0)

    def test_author_cant_delete_attachment_if_no_delete_permission(self):
        self.jon.user_permissions.remove(self.del_permission)

        self.client.login(**self.cred_jon)
        self._upload_testfile()
        att = Attachment.objects.first()
        del_url = reverse('attachments:delete', kwargs={'attachment_pk': att.pk,})
        self.client.get(del_url, follow=True)
        self.assertEqual(Attachment.objects.count(), 1)

    def test_author_cant_delete_others_attachment(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        obj1 = Attachment.objects.order_by('-created')[0]

        self.client.login(**self.cred_jane)
        self._upload_testfile()
        obj2 = Attachment.objects.order_by('-created')[0]

        self.assertNotEqual(obj1, obj2)

        # Jon can't delete Janes attachment
        self.client.login(**self.cred_jon)
        del_url = reverse('attachments:delete', kwargs={'attachment_pk': obj2.pk,})
        self.client.get(del_url, follow=True)

        self.assertEqual(Attachment.objects.count(), 2)

    def test_author_can_delete_others_attachment_with_permission(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        obj1 = Attachment.objects.order_by('-created')[0]

        self.client.login(**self.cred_jane)
        self._upload_testfile()
        obj2 = Attachment.objects.order_by('-created')[0]

        self.assertNotEqual(obj1, obj2)

        # Jon has the `delete_foreign_attachments` permission so he can
        # delete Janes attachment
        self.jon.user_permissions.add(self.del_foreign_permission)
        self.client.login(**self.cred_jon)

        del_url = reverse('attachments:delete', kwargs={'attachment_pk': obj2.pk,})
        self.client.get(del_url, follow=True)

        self.assertEqual(Attachment.objects.count(), 1)
