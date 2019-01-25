from django.contrib import admin

from ...admin import AttachmentInlines
from .models import TestModel


class TestModelAdmin(admin.ModelAdmin):
    inlines = [AttachmentInlines]


admin.site.register(TestModel, TestModelAdmin)
