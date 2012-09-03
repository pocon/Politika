"""
A management command which Grabs MPs Q And A profiles from OA

"""

from django.core.management.base import NoArgsCommand
from members.models import *
from BeautifulSoup import BeautifulStoneSoup as BS
import urllib2

class Command(NoArgsCommand):
    help = "Grab All Members QandA Bio and Add them Into the DB"

    def handle_noargs(self, **options):        
        page = BS(urllib2.urlopen("http://data.openaustralia.org/members/links-abc-qanda.xml"))

        for member in page.findAll("personinfo"):
            m = Member.objects.get(oa_id=member['id'])
            m.qanda = member['mp_biography_qanda']
            m.save()


