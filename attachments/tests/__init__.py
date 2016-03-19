#from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
#from django.core.urlresolvers import reverse
from .models import TestItem

class AttachmentsTestCase(TestCase):
    def setUp(self):
        TestItem.objects.create(title='My first test item')

    # def test_upload(self):
    #     add_url = reverse('attachments:add', kwargs={
    #         'app_label': 'attachments',
    #         'model_name': 'TestModel',
    #         'pk': 1,
    #     })

    #     f = SimpleUploadedFile("avatar.jpg", "file content", content_type="image/jpeg")
    #     self.client.post(add_url, {'attachment_file': f})
