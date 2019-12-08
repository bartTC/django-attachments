Changelog:
==========

v1.5 (2019-12-08)
-----------------

- Dropped support for Python 3.4.
- Added suport for Python 3.8.
- Django 3.0 compatibility and tests.
- Django 2.2 compatibility and tests.

v1.4.1 (2019-07-22)
-------------------

- The templatetags now allow an optional `next` parameter.

v1.4 (2019-02-14)
-----------------

- Dropped Support for Django <=1.10.
- Fixed 'next' URL argument redirect.

v1.3.1 (2019-01-24):
--------------------

- Django 2.1 and Python 3.7 support.
- General code cleanup.

v1.3 (2018-01-09):
------------------

- Added a missing database migration.
- New templatetag ``attachments_count``.
- New setting ``DELETE_ATTACHMENTS_FROM_DISK`` to delete attachment files
  if the attachment model is deleted.
- New setting ``FILE_UPLOAD_MAX_SIZE`` to deny file uploads exceeding this
  value.

v1.2 (2017-12-15):
------------------

- Django 1.11 and 2.0 compatibility and tests.

v1.1 (2017-03-18):
------------------

- Django 1.10 compatibility and tests.
- Python 3.6 compatibility and tests.
- Fixes problems where models have a foreign key named something other
  than "id".

v1.0.1 (2016-06-12):
--------------------

- Added finnish translation.
- Minor test suite improvements.

v1.0 (2016-03-19):
------------------

- General code cleanup to keep compatibility with the latest Django
  (currently 1.8 upwards) as well as Python3. Introduced full testsuite.

- *Backwards incompatible*: The attachment views now use a urlpattern
  ``namespace`` so you need to adjust the urlpattern::

    url(r'^attachments/', include('attachments.urls', namespace='attachments')),

- *Backwards incompatible*: The quotes around the ``as`` variable name
   must be removed::

     {% get_attachments_for entry as "my_entry_attachments" %}

     becomes

     {% get_attachments_for entry as my_entry_attachments %}

- *Possibly backwards incompatible*: The old version had bugs around
   permissions and were not enforcing it in all places. From now on the
   related permissions ``add_attachment`` and ``delete_attachment`` must
   been applied to all related users.

v0.3.1 (2009-07-29):
--------------------

- Added a note to the README that you should secure your static files.

v0.3 (2009-07-22):
------------------

- This version adds more granular control about user permissons. You need
  to explicitly add permissions to users who should been able to upload,
  delete or delete foreign attachments.

  This might be *backwards incompatible* as you did not need to assign
  add/delete permissions before!
