==================
django-attachments
==================

django-attachments is a generic set of template tags to attach any kind of
files to models.

Installation:
=============

1. Put ``attachments`` to your ``INSTALLED_APPS`` in your ``settings.py``
   within your django project.

2. Add ``(r'^attachments/', include('attachments.urls')),`` to your ``urls.py``.
   
This app provides a additional permission ``delete_foreign_attachments``
which enables that users with it can delete foreign attachments. Normally only
the user who uploaded the attachment can delete it.

Usage:
======

In contrib.admin:
-----------------

django-attachments provides a inline object to add a list of attachments to
any kind of model in your admin app.

Simply add ``AttachmentInlines`` to the admin options of your model. Example::

    from django.contrib import admin
    from attachments.admin import AttachmentInlines
    
    class MyEntryOptions(admin.ModelAdmin)
        inlines = [AttachmentInlines]

.. image:: http://cloud.github.com/downloads/bartTC/django-attachments/attachments_screenshot_admin.png

In your frontend templates:
---------------------------

django-attachments comes with some templatetags to add or delete attachments
for your model objects in your frontend.

1. ``get_attachments_for [object]``: Fetches the attachments for the given
   model instance. You can optionally define a variable name in which the attachment
   list is stored in the template context. The default context variable name is
   ``attachments`` Example::
   
   {% get_attachments_for entry as "attachments_list" %}

2. ``attachment_form``: Renders a upload form to add attachments for the given
   model instance. Example::
   
    {% attachment_form [object] %}

   It returns an empty string if the current user is not logged in.

3. ``attachment_delete_link``: Renders a link to the delete view for the given
   *attachment*. Example::
   
    {% for att in attachment_list %}
        {{ att }} {% attachment_delete_link att %}
    {% endfor %}
    
   This tag automatically checks for permission. It returns only a html link if the
   give n attachment's creator is the current logged in user or the user has the 
   ``delete_foreign_attachments`` permission.

Quick Example:
==============

::
    
    {% load attachments_tags %}
    {% get_attachments_for entry as "my_entry_attachments" %}
    
    {% if my_entry_attachments %}
    <ul>
    {% for attachment in my_entry_attachments %}
        <li>
            <a href="{{ attachment.attachment_file.url }}">{{ attachment.filename }}</a>
            {% attachment_delete_link attachment %}
        </li>
    {% endfor %}
    </ul>
    {% endif %}

    {% attachment_form entry %}