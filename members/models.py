from django.db import models

class Electorate(models.Model):
    electorate = models.CharField(max_length=256)
    abc = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.electorate

class Party(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

class Member(models.Model):
    oa_id = models.CharField(max_length=256) #ID in openaustralia: should be of form uk.org.publicwhip/member/x
    oa_matchid = models.CharField(max_length=256) # Match ID in OA, should be of form above
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
    
    news = models.ForeignKey(MPNews, null=True, blank=True)

    def __unicode__(self):
        return self.full_name

class MPNews(models.Model): # This is here so that there is also link1.
    link1 = models.URLField()
    articles = models.ManyToManyField(MPNewsArticle, null=True, blank=True)
    
    def __unicode__(self):
        return self.link1 # for lack of a better one
    
class MPNewsArticle(models.Model):
    title = models.CharField(max_length=128)
    link = models.URLField()
    description = models.CharField(max_length=4096)
    pubDate = models.DateTimeField()
    
    def __unicode__(self):
        return self.title
