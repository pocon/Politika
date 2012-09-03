from django.db import models
from members.models import Member

class MemberPair(models.Model):
	Member1 = models.ForeignKey(Member) # We could make this be Labor, in general
	Member2 = models.ForeignKey(Member) # and this Coalition; but I'm not sure it'd ever matter.
	
	def __unicode__(self):
		return self.Member1.full_name + " & " + self.Member2.full_name

class Vote(models.Model):
	oa_id = models.CharField(max_length=256)   # of form uk.org.publicwhip/debate/yyyy-mm-dd.x.y
	name = models.CharField(max_length=512, blank=True, null=True)    # A title of what is being voted on
	motion = models.CharField(max_length=1024, blank=True, null=True) # The actual motion, for "I move: ..." Blank for bills?
	#bill = models.ForeignKey(Bill, blank=True, null=True) # when we have a Bill model.
	
	mover = models.ForeignKey(Member, blank=True, null=True)
	seconder = models.ForeignKey(Member, blank=True, null=True)
	
	ayes = models.ManyToManyField(Member, blank=True, null=True)
	noes = models.ManyToManyField(Member, blank=True, null=True)
	pairs = models.ManyToManyField(MemberPair, blank=True, null=True)
	
	def __unicode__(self):
		return self.name   
