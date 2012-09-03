from django.db import models
from members.models import Member

class MemberPair(models.Model):
	LaborMP = models.ForeignKey(Member)
	CoalitionMP = models.ForeignKey(Member)
	
	def __unicode__(self):
		return self.LaborMP.full_name + " & " + self.CoalitionMP.full_name

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