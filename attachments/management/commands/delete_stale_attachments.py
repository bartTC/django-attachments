from django.core.management.base import BaseCommand

from attachments.models import Attachment
from attachments.views import remove_file_from_disk


class Command(BaseCommand):
    help = ("Remove attachments for which the related objects "
            "don't exist anymore!")

    def add_arguments(self, parser):
        parser.add_argument(
            '-y', '--yes', default='x', action='store_const', const='y',
            dest='answer', help='Automatically confirm deletion',
        )

    def handle(self, *args, **kwargs):
        verbose = kwargs['verbosity'] >= 1
        answer = kwargs['answer']

        # -v0 sets --yes
        if not verbose:
            answer = 'y'

        for att in Attachment.objects.all():
            if att.content_object is None:
                if verbose:
                    self.stdout.write(
                        "Attachment `%s' to non-existing `%s' with PK `%s'" %
                        (att, att.content_type.model, att.object_id))

                while answer not in 'yn':
                    answer = input("Do you wish to delete? [yN] ")
                    if not answer:
                        answer = 'x'
                        continue
                    answer = answer[0].lower()

                if answer == 'y' :
                    remove_file_from_disk(att.attachment_file)
                    att.delete()

                    if verbose:
                        self.stdout.write("Deleted attachment `%s'" % att)
