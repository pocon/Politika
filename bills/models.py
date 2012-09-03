from django.db import models
from django.auth.models import User
import datetime

class Edit(models.Model):
    object_id = models.IntegerField()
    object_type = models.CharField(max_length=128) # Issue, Bill or Ammendment

    editor = models.ForeignKey(User)
    time = models.DateTimeField()

    title = models.CharField(max_length=128)
    summary = models.TextField(max_length=2048, blank=True, null=True)
    detailed = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.time = datetime.datetime.now()
        super(User, self).save(*args, **kwargs)

class Issue(models.Model):
    title = models.CharField(max_length=128)
    summary = models.TextField(max_length=2048, blank=True, null=True)

    detailed = models.TextField(blank=True, null=True)


class Bill(models.Model):
    title = models.CharField(max_length=256)
    summary = models.TextField(max_length=2048, blank=True, null=True)

    detailed = models.TextField(blank=True, null=True)

    introduced = models.DateField()
    introduced_by = models.ForeignKey(Member, blank=True, null=True)

class Ammendment(models.Model):
    title = models.CharField(max_length=256)
    summary = models.TextField(max_length=2048, blank=True, null=True)

    detailed = models.TextField(blank=True, null=True)

    introduced = models.DateField()
    introduced_by = models.ForeignKey(Member, blank=True, null=True)
