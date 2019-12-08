from django.db import models


class TestModel(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        db_table = "testapp_testmodel"

    def get_absolute_url(self):
        return "/"
