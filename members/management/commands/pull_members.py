"""
A management command which Grabs MPs from OA

"""

from django.core.management.base import NoArgsCommand
from members.models import *
from BeautifulSoup import BeautifulStoneSoup as BS
import urllib2

class Command(NoArgsCommand):
    help = "Grab All Members and Add them Into the DB"

    def handle_noargs(self, **options):        
        page = BS(urllib2.urlopen("http://data.openaustralia.org/members/people.xml"))

        for member in page.findAll("person"):
            mid = False
            for office in member.findAll("office"):
                if office.get("current", "no") == "yes":
                    if office['id'].startswith("uk.org.publicwhip/member/"):
                        mid = office['id']
            Member(name=member['latestname'], oa_id=member['id'], oa_matchid=mid).save()
