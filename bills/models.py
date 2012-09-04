from django.db import models
from django.auth.models import User
import datetime

class Edit(models.Model):
    object_id = models.IntegerField()
    object_type = models.CharField(max_length=128) # Issue, Bill or Ammendment

    editor = models.ForeignKey(User)
    time = models.DateTimeField(blank=True)
    moderated = models.BooleanField(default=False)

    title = models.CharField(max_length=128)
    summary = models.TextField(max_length=2048, blank=True, null=True)
    detailed = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.time = datetime.datetime.now()
        super(User, self).save(*args, **kwargs)

class Link(models.Model):
    text = models.CharField(max_length=256)
    link = models.URLField()


class Flag(models.Model):
    edit = models.ForeignKey(Edit)
    
    flagger = models.ForeignKey(User)
    time = models.DateTimeField(blank=True)
    
    subject = models.CharField(max_length=128)
    reason = models.TextField()

    sustained = models.BooleanField(default=False) # If choose to uphold flag (eg: edit should be reverted)
    overturned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.time = datetime.datetime.now()
        super(User, self).save(*args, **kwargs)

    def sustain(self, admin):
        self.sustained = True
        self.save()
        self.edit.moderated = True
        self.edit.save()

    def overturned(self, admin):
        self.overturned = True
        self.save()

class Issue(models.Model):
    title = models.CharField(max_length=128)
    summary = models.TextField(max_length=2048, blank=True, null=True)

    detailed = models.TextField(blank=True, null=True)

    def flag(self, flagger, subject, reason):
        e = Edit.objects.filter(object_id=self.id).filter(object_type="Issue").filter(moderated=False).order_by('-time')
        Flag(edit=e, flagger=flagger, subject=subject, reason=reason).save()

    def edit_history(self):
        return Edit.objects.filter(object_id=self.id).filter(object_type="Issue").order_by('-time')

    def edit(self, editor, title, summary, detailed):
        Edit(
            object_id = self.id,
            object_type = "Issue",
            editor = editor,
            title = title,
            summary = summary,
            detailed = detailed,
            ).save()

        self.title = title
        self.summary = summary
        self.detailed = detailed
        self.save()


class Bill(models.Model):
    title = models.CharField(max_length=256)
    summary = models.TextField(max_length=2048, blank=True, null=True)

    detailed = models.TextField(blank=True, null=True)

    introduced = models.DateField()
    introduced_by = models.ForeignKey(Member, blank=True, null=True)

    links = models.ManyToManyField(blank=True, null=True)

    def flag(self, flagger, subject, reason):
        e = Edit.objects.filter(object_id=self.id).filter(object_type="Bill").filter(moderated=False).order_by('-time')
        Flag(edit=e, flagger=flagger, subject=subject, reason=reason).save()

    def edit_history(self):
        return Edit.objects.filter(object_id=self.id).filter(object_type="Bill").order_by('-time')

    def edit(self, editor, title, summary, detailed):
        Edit(
            object_id = self.id,
            object_type = "Bill",
            editor = editor,
            title = title,
            summary = summary,
            detailed = detailed,
            ).save()

        self.title = title
        self.summary = summary
        self.detailed = detailed
        self.save()

class Ammendment(models.Model):
    title = models.CharField(max_length=256)
    summary = models.TextField(max_length=2048, blank=True, null=True)

    detailed = models.TextField(blank=True, null=True)

    introduced = models.DateField()
    introduced_by = models.ForeignKey(Member, blank=True, null=True)

    def flag(self, flagger, subject, reason):
        e = Edit.objects.filter(object_id=self.id).filter(object_type="Ammendment").filter(moderated=False).order_by('-time')
        Flag(edit=e, flagger=flagger, subject=subject, reason=reason).save()

    def edit_history(self):
        return Edit.objects.filter(object_id=self.id).filter(object_type="Ammendment").order_by('-time')

    def edit(self, editor, title, summary, detailed):
        Edit(
            object_id = self.id,
            object_type = "Ammendment",
            editor = editor,
            title = title,
            summary = summary,
            detailed = detailed,
            ).save()

        self.title = title
        self.summary = summary
        self.detailed = detailed
        self.save()

class Malicious_Edit(models.Model):
    flag = models.ForeignKey(Flag)
    admin = models.ForeignKey(User)


