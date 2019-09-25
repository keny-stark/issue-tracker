from django.db import models


class Tracker(models.Model):
    summary = models.TextField(max_length=100, null=False, blank=False, verbose_name='Summary')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Description')
    status = models.ForeignKey('webapp.Status', related_name='tracker', on_delete=models.PROTECT, verbose_name='Status')
    type = models.ForeignKey('webapp.Type', related_name='tracker', on_delete=models.PROTECT, verbose_name='Type')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Time of add')

    def __str__(self):
        return self.summary


class Type(models.Model):
    type = models.CharField(max_length=40, null=False, blank=False, verbose_name='Type')

    def __str__(self):
        return self.type


class Status(models.Model):
    status = models.CharField(max_length=40, null=False, blank=False, verbose_name='Status')

    def __str__(self):
        return self.status
