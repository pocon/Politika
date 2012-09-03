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

    def __unicode__(self):
        return self.full_name

class MemberPair(models.Model):
	LaborMP = models.ForeignKey(Member)
	CoalitionMP = models.ForeignKey(Member)
	
	def __unicode__(self):
		return self.LaborMP.full_name + " & " + self.CoalitionMP.full_name

class Vote(models.Model):
	oa_id = models.CharField(max_length=256)   # of form uk.org.publicwhip/debate/yyyy-mm-dd.x.y
	name = models.CharField(max_length=512)    # A title of what is being voted on
	motion = models.CharField(max_length=1024, blank=True) # The actual motion, for "I move: ..." Blank for bills?
	#bill = models.ForeignKey(Bill, blank=True, null=True) # when we have a Bill model.
	
	mover = models.ForeignKey(Member, blank=True, null=True)
	seconder = models.ForeignKey(Member, blank=True, null=True)
	
	ayes = models.ManyToManyField(Member, blank=True, null=True)
	noes = models.ManyToManyField(Member, blank=True, null=True)
	pairs = models.ManyToManyField(MemberPair, blank=True, null=True)
	
	def __unicode__(self):
		return self.name   