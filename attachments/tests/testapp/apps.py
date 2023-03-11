"""
Custom app config to demonstrate and test the 'custom attachment validators'
functionality.
"""

from attachments.apps import AttachmentsConfig
from django.forms import ValidationError


def deny_xml_uploads(uploaded_file):
    if uploaded_file.read().find(b"<xml>") > -1:
        raise ValidationError("XML is forbidden")


class CustomizedAttachmentsApp(AttachmentsConfig):
    """
    Adds a custom form validator function.
    """
    attachment_validators = (deny_xml_uploads,)
