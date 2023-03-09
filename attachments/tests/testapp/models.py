import uuid
from django.db import models


class TestModel(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        db_table = "testapp_testmodel"

    def get_absolute_url(self):
        return "/"


class ModelWithUuidPk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)

    class Meta:
        db_table = "testapp_uuid4_model"

    def get_absolute_url(self):
        return "/"
