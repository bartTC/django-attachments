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

    def test_no_attachments_by_default(self):
        self.assertEqual(Attachment.objects.count(), 0)
        self.assertEqual(Attachment.objects.attachments_for_object(self.obj).count(), 0)

    def test_upload(self):
            add_url = reverse('attachments:add', kwargs={
                'app_label': 'testapp',
                'model_name': 'testmodel',
                'pk': self.obj.pk,
            })

            f = SimpleUploadedFile("avatar.jpg", b"file content", content_type="image/jpeg")
            self.client.post(add_url, {'attachment_file': f}, follow=True)
            self.assertEqual(Attachment.objects.count(), 1)
            self.assertEqual(Attachment.objects.attachments_for_object(self.obj).count(), 1)
