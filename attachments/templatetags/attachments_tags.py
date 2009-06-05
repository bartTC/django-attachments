from django.template import Library, Node, Variable
from attachments.forms import AttachmentForm
from attachments.views import add_url_for_obj
from django.core.urlresolvers import reverse
from attachments.models import Attachment

register = Library()

@register.inclusion_tag('attachments/add_form.html', takes_context=True)
def attachment_form(context, obj):
    """
    Renders a "upload attachment" form
    """
    if context['user'].is_authenticated():
        return {
            'form': AttachmentForm(),
            'form_url': add_url_for_obj(obj),
            'next': context['request'].build_absolute_uri(),
        }
    else:
        return {
            'form': None,
        }

@register.inclusion_tag('attachments/delete_link.html', takes_context=True)
def attachment_delete_link(context, attachment):
    """
    Renders a html link to the delete view of the given attachment. Returns
    no content if the request-user has no permission to delete foreign
    attachments.
    """
    if context['user'].has_perm('delete_foreign_attachments') \
       or context['user'] == attachment.creator:
        return {
            'next': context['request'].build_absolute_uri(),
            'delete_url': reverse('delete_attachment', kwargs={'attachment_pk': attachment.pk})
        }
    return {'delete_url': None,}



class AttachmentsForObjectNode(Node):
    def __init__(self, obj, var_name):
        self.obj = obj
        self.var_name = var_name

    def resolve(self, var, context):
        """Resolves a variable out of context if it's not in quotes"""
        if var[0] in ('"', "'") and var[-1] == var[0]:
            return var[1:-1]
        else:
            return Variable(var).resolve(context)

    def render(self, context):
        obj = self.resolve(self.obj, context)
        var_name = self.resolve(self.var_name, context)
        print var_name
        context[var_name] = Attachment.objects.attachments_for_object(obj)
        return ''

@register.tag
def get_attachments_for(parser, token):
    """
    Resolves attachments that are attached to a given object. You can specify
    the variable name in the context the attachments are stored using the `as`
    argument. Default context variable name is `attachments`.

    Syntax::

        {% get_attachments_for obj %}
        {% for att in attachments %}
            {{ att }}
        {% endfor %}

        {% get_attachments_for obj as "my_attachments" %}

    """
    def next_bit_for(bits, key, if_none=None):
        try:
            return bits[bits.index(key)+1]
        except ValueError:
            return if_none

    bits = token.contents.split()
    args = {
        'obj': next_bit_for(bits, 'get_attachments_for'),
        'var_name': next_bit_for(bits, 'as', '"attachments"'),
    }
    return AttachmentsForObjectNode(**args)