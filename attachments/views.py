from __future__ import unicode_literals

from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from attachments.models import Attachment
from attachments.forms import AttachmentForm

try:
    from django.db.models.loading import get_model
except ImportError:
    from django.apps import apps
    get_model = apps.get_model


def add_url_for_obj(obj):
    return reverse('attachments:add', kwargs={
        'app_label': obj._meta.app_label,
        'model_name': obj._meta.model_name,
        'pk': obj.pk
    })

@require_POST
@login_required
def add_attachment(request, app_label, model_name, pk,
                   template_name='attachments/add.html', extra_context={}):
    next = request.POST.get('next', '/')
    model = get_model(app_label, model_name)
    if model is None:
        return HttpResponseRedirect(next)
    obj = get_object_or_404(model, pk=pk)
    form = AttachmentForm(request.POST, request.FILES)

    if form.is_valid():
        form.save(request, obj)
        messages.success(request, ugettext('Your attachment was uploaded.'))
        return HttpResponseRedirect(next)

    template_context = {
        'form': form,
        'form_url': add_url_for_obj(obj),
        'next': next,
    }
    template_context.update(extra_context)
    return render_to_response(template_name, template_context,
                              RequestContext(request))

@login_required
def delete_attachment(request, attachment_pk):
    g = get_object_or_404(Attachment, pk=attachment_pk)
    if request.user.has_perm('delete_foreign_attachments') \
       or request.user == g.creator:
        g.delete()
        messages.success(request, ugettext('Your attachment was deleted.'))
    next = request.REQUEST.get('next') or '/'
    return HttpResponseRedirect(next)
