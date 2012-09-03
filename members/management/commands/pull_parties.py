"""
A management command which Grabs Parties and their members from OA

"""

from django.core.management.base import NoArgsCommand
from members.models import *
from BeautifulSoup import BeautifulStoneSoup as BS
import urllib2

class Command(NoArgsCommand):
    help = "Grab All Parties and Add them Into the DB with Member"

    def handle_noargs(self, **options):        
        page = BS(urllib2.urlopen("http://data.openaustralia.org/members/representatives.xml"))

        for member in page.findAll("member"):
            if member['todate'] == "9999-12-31":
                try:
                    p = Party.objects.get(name=member['party'])
                except:
                    p = Party(name=member['party'])
                    p.save()

                m = Member.objects.get(oa_id=member['id'])
                m.party = p
                m.save()



