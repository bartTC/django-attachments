.. image:: https://travis-ci.org/bartTC/django-attachments.svg?branch=master
    :target: https://travis-ci.org/bartTC/django-attachments

.. image:: https://codecov.io/github/bartTC/django-attachments/coverage.svg?branch=master
    :target: https://codecov.io/github/bartTC/django-attachments?branch=master

==================
django-attachments
==================

django-attachments is a generic set of template tags to attach any kind of
files to models.

Installation:
=============

1. Put ``attachments`` to your ``INSTALLED_APPS`` in your ``settings.py``
   within your django project::

    INSTALLED_APPS = (
        ...
        'attachments',
    )

2. Add the attachments urlpattern to your ``urls.py``::

    url(r'^attachments/', include('attachments.urls', namespace='attachments')),

3. Migrate your database::

    ./manage.py migrate

5. Grant the user some permissions:

   * For **adding attachments** grant the user (or group) the permission
     ``attachments.add_attachment``.

   * For **deleting attachments** grant the user (or group) the permission
     ``attachments.delete_attachment``. This allows the user to delete their
     attachments only.

   * For **deleting foreign attachments** (attachments by other users) grant
     the user the permission ``attachments.delete_foreign_attachments``.

6. Set ``DELETE_ATTACHMENTS_FROM_DISK`` to ``True`` if you want to remove
   files from disk when Attachment objects are removed!

7. Configure ``FILE_UPLOAD_MAX_SIZE`` (optional). This is the maximum size in
   bytes before raising form validation errors. If not set there is no restriction
   on file size.

Mind that you serve files!
==========================

django-attachments stores the files in your site_media directory and does not modify
them. For example, if an user uploads a .html file your webserver will probably display
it in HTML. It's a good idea to serve such files as plain text. In a Apache2
configuration this would look like::

    <Location /site_media/attachments>
        AddType text/plain .html .htm .shtml .php .php5 .php4 .pl .cgi
    </Location>


Tests
=====

Run the testsuite in your local environment using ``pipenv``::

    $ cd django-attachments/
    $ pipenv install
    $ pipenv run ./runtests.py

Or use tox to test against various Django and Python versions::

    $ tox -r

You can also invoke the test suite or other 'manage.py' commands by calling
the ``django-admin`` tool with the test app settings::

    $ cd django-attachments/
    $ pipenv install
    $ pipenv run django-admin.py migrate
    $ pipenv run django-admin.py runserver

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
        inlines = (AttachmentInlines,)

.. image:: http://cloud.github.com/downloads/bartTC/django-attachments/attachments_screenshot_admin.png

In your frontend templates:
---------------------------

First of all, load the attachments_tags in every template you want to use it::

    {% load attachments_tags %}

django-attachments comes with some templatetags to add or delete attachments
for your model objects in your frontend.

1. ``get_attachments_for [object]``: Fetches the attachments for the given
   model instance. You can optionally define a variable name in which the attachment
   list is stored in the template context (this is required in Django 1.8). If
   you do not define a variable name, the result is printed instead.

   {% get_attachments_for entry as "attachments_list" %}

2. ``attachments_count [object]``: Counts the attachments for the given
   model instance and returns an int::

   {% attachments_count entry %}

3. ``attachment_form``: Renders a upload form to add attachments for the given
   model instance. Example::

    {% attachment_form [object] %}

   It returns an empty string if the current user is not logged in.

4. ``attachment_delete_link``: Renders a link to the delete view for the given
   *attachment*. Example::

    {% for att in attachments_list %}
        {{ att }} {% attachment_delete_link att %}
    {% endfor %}

   This tag automatically checks for permission. It returns only a html link if the
   give n attachment's creator is the current logged in user or the user has the
   ``delete_foreign_attachments`` permission.

Quick Example:
==============

::

    {% load attachments_tags %}
    {% get_attachments_for entry as my_entry_attachments %}

    <span>Object has {% attachments_count entry %} attachments</span>
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

    {% if messages %}
    <ul class="messages">
    {% for message in messages %}
        <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>
            {{ message }}
        </li>
    {% endfor %}
    </ul>
    {% endif %}
