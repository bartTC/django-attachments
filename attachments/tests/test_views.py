from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase

from attachments.models import Attachment

from .testapp.models import TestModel


class AttachmentsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('jon', 'jon@foobar.com', 'foobar')
        self.obj = TestModel.objects.create(title='My first test item')
        self.client.login(username='jon', password='foobar')

    def _upload_testfile(self):
        add_url = reverse('attachments:add', kwargs={
            'app_label': 'testapp',
            'model_name': 'testmodel',
            'pk': self.obj.pk,
        })
        f = SimpleUploadedFile("avatar.jpg", b"file content",
                               content_type="image/jpeg")
        return self.client.post(add_url, {'attachment_file': f}, follow=True)

    def test_empty_post_to_form_wont_create_attachment(self):
        add_url = reverse('attachments:add', kwargs={
            'app_label': 'testapp',
            'model_name': 'testmodel',
            'pk': self.obj.pk,
        })
        response = self.client.post(add_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(Attachment.objects.count(), 0)
        self.assertEqual(Attachment.objects.attachments_for_object(self.obj).count(), 0)

    def test_invalid_model_wont_fail(self):
        add_url = reverse('attachments:add', kwargs={
            'app_label': 'thisdoes',
            'model_name': 'notexist',
            'pk': self.obj.pk,
        })
        response = self.client.post(add_url)
        self.assertEqual(302, response.status_code) # Redirect to 'next' page
        self.assertEqual(Attachment.objects.count(), 0)
        self.assertEqual(Attachment.objects.attachments_for_object(self.obj).count(), 0)

    def test_no_attachments_by_default(self):
        self.assertEqual(Attachment.objects.count(), 0)
        self.assertEqual(Attachment.objects.attachments_for_object(self.obj).count(), 0)

    def test_upload(self):
        self._upload_testfile()
        self.assertEqual(Attachment.objects.count(), 1)
        self.assertEqual(Attachment.objects.attachments_for_object(self.obj).count(), 1)

    def test_unauthed_user_cant_delete_attachment(self):
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
        self._upload_testfile()
        att = Attachment.objects.first()
        del_url = reverse('attachments:delete', kwargs={'attachment_pk': att.pk,})
        self.client.get(del_url, follow=True)
        self.assertEqual(Attachment.objects.count(), 0)
