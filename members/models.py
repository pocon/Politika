from django.db import models

class Electorate(models.Model):
    electorate = models.CharField(max_length=256)

    def __unicode__(self):
        return self.electorate

class Party(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

class Member(models.Model):
    oa_id = models.CharField(max_length=256) #ID in openaustralia: should be of form uk.org.publicwhip/member/x
    name = models.CharField(max_length=128)

    website = models.URLField(null=True, blank=True)
    aph_page = models.URLField(null=True, blank=True)
    wikipedia = models.URLField(null=True, blank=True)
    twitter = models.CharField(max_length=128, null=True, blank=True) # Just contains their handle
    qanda = models.URLField(null=True, blank=True)

    position = models.CharField(max_length=256, null=True, blank=True)
    party = models.ForeignKey(Party, null=True, blank=True)
    electorate = models.ForeignKey(Electorate, null=True, blank=True)
    
    simage = models.ImageField(null=True, blank=True) # Small Image
    bimage = models.ImageField(null=True, blank=True) # Big Image

    def __unicode__(self):
        return self.full_name
    
