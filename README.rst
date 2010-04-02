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

3. Add ``'django.core.context_processors.request'`` to your ``TEMPLATE_CONTEXT_PROCESSORS``
   in your settings.py. If this setting does not exist, simply add the following
   snippet at the end of your settings.py::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.auth',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.request',
    )

4. Don't forget to resync your database::

    ./manage.py syncdb

5. Grant the user some permissons:

   * For **adding attachments** grant the user (or group) the permission
     ``attachments.add_attachments``.

   * For **deleting attachments** grant the user (or group) the permission
     ``attachments.delete_attachments``. This allows the user to delete only
     attachments which are assigned to him (rather the attachments he uploaded self).

   * For **deleting foreign attachments** (attachments by other users) grant
     the user the permission ``attachments.delete_foreign_attachments``.
     
   This only works for the templatetags, the admin still allows anybody to add
   or delete attachments.


Mind that you serve files!
==========================

django-attachments stores the files in your site_media directory and does not modify
them. For example, if an user uploads a .html file your webserver will probably display
it in HTML. It's a good idea to serve such files as plain text. In a Apache2
configuration this would look like:: 

    <Location /site_media/attachments>
        AddType text/plain .html .htm .shtml .php .php5 .php4 .pl .cgi
    </Location>


Usage:
======

In contrib.admin:
-----------------

django-attachments provides a inline object to add a list of attachments to
any kind of model in your admin app.

Simply add ``AttachmentInlines`` to the admin options of your model. Example::

    from django.contrib import admin
    from attachments.admin import AttachmentInlines

    class MyEntryOptions(admin.ModelAdmin):
        inlines = [AttachmentInlines]

.. image:: http://cloud.github.com/downloads/bartTC/django-attachments/attachments_screenshot_admin.png

In your frontend templates:
---------------------------

First of all, load the attachments_tags in every template you want to use it::

    {% load attachments_tags %}
    
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

In the console:
===============

First, import the items you will need::

    import os
    from django.core.files import File
    from attachments.models import Attachment
    from myproject.models import Person

Next, retrieve the object you wish to attach to::

    me = Person.objects.get(name='aaron')

Now open the attachment you want from your drive using the django File object::

    mypicture = File(open('/home/aaron/mypicture.jpg', 'r'))

Finally, create the Attachment object and save it::

    a = Attachment()
    a.creator = me
    a.attachment_file = mypicture
    a.save()

Changelog:
==========

v0.3.1 (2009-07-29):

    * Added a note to the README that you should secure your static files.

v0.3 (2009-07-22):

    * This version adds more granular control about user permissons. You need
      to explicitly add permissions to users who should been able to upload,
      delete or delete foreign attachments. 

      This might be **backwards incompatible** as you did not need to assign add/delete
      permissions before!
