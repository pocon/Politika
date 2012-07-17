from django.db import models

class Website(models.Model):
    text = models.CharField(max_length=256)
    url = models.URLField()
    
    def __unicode__(self):
        return self.text

class Position(models.Model):
    position = models.CharField(max_length=256)
    primary = models.BooleanField() # whether this is the most important position they hold

    def __unicode__(self):
        return self.position

class Electorate(models.Model):
    electorate = models.CharField(max_length=256)
    state = models.CharField(max_length=128)

    def __unicode__(self):
        return self.electorate + ', ' + self.state

class Party(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

class Member(models.Model):
    mpid = models.CharField(max_length=20)
    profile_full_url = models.URLField() # Shouldn't really be used unless a problem with below
    url = models.URLField() # for the pretty/short version that APH provides which redirects to page
    websites = models.ManyToManyField(Website, null=True, blank=True)
    positions = models.ManyToManyField(Position, null=True, blank=True)
    party = models.ForeignKey(Party, null=True, blank=True)
    electorate = models.ForeignKey(Electorate)
    
    name = models.CharField(max_length=128) # Just First + Last
    full_name = models.CharField(max_length=256) # Incl. 'The Hon' and MP, MR, etc.
    vote_name = models.CharField(max_length=256)
    
    
    image = models.URLField()

    def __unicode__(self):
        return self.full_name
    
