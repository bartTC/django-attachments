from django.template import Library
from django.urls import reverse

from ..forms import AttachmentForm
from ..models import Attachment
from ..views import add_url_for_obj

register = Library()


@register.inclusion_tag("attachments/add_form.html", takes_context=True)
def attachment_form(context, obj, **kwargs):
    """
    Renders a "upload attachment" form.

    The user must own ``attachments.add_attachment permission`` to add
    attachments.
    """
    if context["user"].has_perm("attachments.add_attachment"):
        return {
            "form": AttachmentForm(),
            "form_url": add_url_for_obj(obj),
            "next": kwargs.get("next", context.request.build_absolute_uri()),
        }
    else:
        return {"form": None}


@register.inclusion_tag("attachments/delete_link.html", takes_context=True)
def attachment_delete_link(context, attachment, **kwargs):
    """
    Renders a html link to the delete view of the given attachment. Returns
    no content if the request-user has no permission to delete attachments.

    The user must own either the ``attachments.delete_attachment`` permission
    and is the creator of the attachment, that he can delete it or he has
    ``attachments.delete_foreign_attachments`` which allows him to delete all
    attachments.
    """
    if context["user"].has_perm("attachments.delete_foreign_attachments") or (
        context["user"] == attachment.creator
        and context["user"].has_perm("attachments.delete_attachment")
    ):
        return {
            "next": kwargs.get("next", context.request.build_absolute_uri()),
            "delete_url": reverse(
                "attachments:delete", kwargs={"attachment_pk": attachment.pk}
            ),
        }
    return {"delete_url": None}


@register.simple_tag
def attachments_count(obj):
    """
    Counts attachments that are attached to a given object::

        {% attachments_count obj %}
    """
    return Attachment.objects.attachments_for_object(obj).count()


@register.simple_tag
def get_attachments_for(obj, *args, **kwargs):
    """
    Resolves attachments that are attached to a given object. You can specify
    the variable name in the context the attachments are stored using the `as`
    argument.

    Syntax::

        {% get_attachments_for obj as "my_attachments" %}
    """
    return Attachment.objects.attachments_for_object(obj)
