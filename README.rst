.. image:: https://badge.fury.io/py/django-attachments.svg
    :target: https://badge.fury.io/py/django-attachments

.. image:: https://travis-ci.org/bartTC/django-attachments.svg?branch=master
    :target: https://travis-ci.org/bartTC/django-attachments

.. image:: https://api.codacy.com/project/badge/Grade/e13db6df2a2148b08c662798642aa611
    :alt: Codacy Badge
    :target: https://app.codacy.com/app/bartTC/django-attachments

.. image:: https://api.codacy.com/project/badge/Coverage/e13db6df2a2148b08c662798642aa611
    :target: https://www.codacy.com/app/bartTC/django-attachments

==================
django-attachments
==================

django-attachments is a generic set of template tags to attach any kind of
files to models.

Installation:
=============

1. Put ``attachments`` to your ``INSTALLED_APPS`` in your ``settings.py``
   within your django project:
   
   .. code-block:: python

        INSTALLED_APPS = (
            ...
            'attachments',
        )

2. Add the attachments urlpattern to your ``urls.py``:

   .. code-block:: python

        url(r'^attachments/', include('attachments.urls', namespace='attachments')),

3. Migrate your database:

   .. code-block:: shell

        ./manage.py migrate

4. Grant the user some permissions:

   * For **adding attachments** grant the user (or group) the permission
     ``attachments.add_attachment``.

   * For **deleting attachments** grant the user (or group) the permission
     ``attachments.delete_attachment``. This allows the user to delete their
     attachments only.

   * For **deleting foreign attachments** (attachments by other users) grant
     the user the permission ``attachments.delete_foreign_attachments``.

5. Set ``DELETE_ATTACHMENTS_FROM_DISK`` to ``True`` if you want to remove
   files from disk when Attachment objects are removed!

6. Configure ``FILE_UPLOAD_MAX_SIZE`` (optional). This is the maximum size in
   bytes before raising form validation errors. If not set there is no restriction
   on file size.

Mind that you serve files!
==========================

django-attachments stores the files in your site_media directory and does not modify
them. For example, if an user uploads a .html file your webserver will probably display
it in HTML. It's a good idea to serve such files as plain text. In a Apache2
configuration this would look like:

.. code-block:: apache

    <Location /site_media/attachments>
        AddType text/plain .html .htm .shtml .php .php5 .php4 .pl .cgi
    </Location>


House-keeping
=============

django-attachments provides the ``delete_stale_attachments`` management command.
It will remove all attachments for which the related objects don't exist anymore!
Sys-admins could then:

.. code-block:: shell

    ./manage.py delete_stale_attachments

You may also want to execute this via cron.


Local development
=================

Installing a local devel environment with ``pipenv``.
It creates a virtualenv for you with the right ENV variables loaded from ``.env``.

   .. code-block:: shell

        # pip install pipenv

        $ pipenv install
        Loading .env environment variables...
        Installing dependencies from Pipfile.lock (a053bc)...
        To activate this project's virtualenv, run pipenv shell.
        Alternatively, run a command inside the virtualenv with pipenv run.


Tests
=====

Run the testsuite in your local environment using ``pipenv``:

.. code-block:: shell

    $ cd django-attachments/
    $ pipenv install --dev
    $ pipenv run pytest attachments/

Or use tox to test against various Django and Python versions:

.. code-block:: shell

    $ tox -r

You can also invoke the test suite or other 'manage.py' commands by calling
the ``django-admin`` tool with the test app settings:

.. code-block:: shell

    $ cd django-attachments/
    $ pipenv install --dev
    $ pipenv run test
    $ pipenv run django-admin.py runserver
    $ pipenv run django-admin makemigrations --dry-run


Building a new release
======================

   .. code-block:: shell

        $ git tag
        $ change version in setup.cfg
        $ pip install -U setuptools
        $ python setup.py sdist && python setup.py bdist_wheel --universal
        $ twine upload --sign dist/*

Usage:
======

In contrib.admin:
-----------------

django-attachments provides a inline object to add a list of attachments to
any kind of model in your admin app.

Simply add ``AttachmentInlines`` to the admin options of your model. Example:

.. code-block:: python

    from django.contrib import admin
    from attachments.admin import AttachmentInlines

    class MyEntryOptions(admin.ModelAdmin):
        inlines = (AttachmentInlines,)

.. image:: http://cloud.github.com/downloads/bartTC/django-attachments/attachments_screenshot_admin.png

In your frontend templates:
---------------------------

First of all, load the attachments_tags in every template you want to use it:

.. code-block:: html+django

    {% load attachments_tags %}

django-attachments comes with some templatetags to add or delete attachments
for your model objects in your frontend.

1. ``get_attachments_for [object]``: Fetches the attachments for the given
   model instance. You can optionally define a variable name in which the attachment
   list is stored in the template context (this is required in Django 1.8). If
   you do not define a variable name, the result is printed instead.

   .. code-block:: html+django

        {% get_attachments_for entry as attachments_list %}

2. ``attachments_count [object]``: Counts the attachments for the given
   model instance and returns an int:

   .. code-block:: html+django

        {% attachments_count entry %}

3. ``attachment_form``: Renders a upload form to add attachments for the given
   model instance. Example:

   .. code-block:: html+django

        {% attachment_form [object] %}

   It returns an empty string if the current user is not logged in.

4. ``attachment_delete_link``: Renders a link to the delete view for the given
   *attachment*. Example:

   .. code-block:: html+django

        {% for att in attachments_list %}
            {{ att }} {% attachment_delete_link att %}
        {% endfor %}

   This tag automatically checks for permission. It returns only a html link if the
   give n attachment's creator is the current logged in user or the user has the
   ``delete_foreign_attachments`` permission.

Quick Example:
==============

.. code-block:: html+django

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

Settings
========

- ``DELETE_ATTACHMENTS_FROM_DISK`` will delete attachment files when the
  attachment model is deleted. **Default False**!
- ``FILE_UPLOAD_MAX_SIZE`` in bytes. Deny file uploads exceeding this value.
  **Undefined by default**.
- ``AppConfig.attachment_validators`` - a list of custom form validator functions
  which will be executed against uploaded files. If any of them raises
  ``ValidationError`` the upload will be denied. **Empty by default**. See
  ``attachments/tests/testapp/apps.py`` for an example.
