from django.db import models


class ApiAccess(models.Model):
    service = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = 'API token'
        verbose_name_plural = 'Access tokens'

    def __str__(self):
        return '{}'.format(self.service)
