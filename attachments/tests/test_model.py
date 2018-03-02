from attachments.models import Attachment

from .base import BaseTestCase


class ModelTestCase(BaseTestCase):

    def test_str_return_value(self):
        self.client.login(**self.cred_jon)
        self._upload_testfile()
        attachment = Attachment.objects.attachments_for_object(self.obj)[0]
        correct_str = '{0.creator.username} attached {0.attachment_file.name}'.format(attachment)
        self.assertEqual(str(attachment), correct_str)
