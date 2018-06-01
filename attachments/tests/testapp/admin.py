from django.contrib import admin

from attachments.admin import AttachmentInlines
from attachments.tests.testapp.models import TestModel

class TestModelAdmin(admin.ModelAdmin):
    inlines = [AttachmentInlines]

admin.site.register(TestModel, TestModelAdmin)
