==================
django-attachments
==================

django-attachments is a generic set of template tags to attach any kind of
files to any models.

Quick Example:
==============

::

    {% load attachments_tags %}
    {% get_attachments_for entry as "my_wiki_attachments" %}

    {% if my_wiki_attachments %}
    <ul>
    {% for attachment in my_wiki_attachments %}
        <li>
            <a href="{{ attachment.attachment_file.url }}">{{ attachment.filename }}</a>
            {% attachment_delete_link attachment %}
        </li>
    {% endfor %}
    </ul>
    {% endif %}

    {% attachment_form entry %}