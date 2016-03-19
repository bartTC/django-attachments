from django.db import models

class MyTestAppModel(models.Model):
    title = models.CharField(max_length=100)

    def get_absolute_url(self):
        return '/'
