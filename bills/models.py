from django.db import models

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
