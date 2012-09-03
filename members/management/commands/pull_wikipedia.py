"""
A management command which Grabs MPs Wikipedia Pages from OA

"""

from django.core.management.base import NoArgsCommand
from members.models import *
from BeautifulSoup import BeautifulStoneSoup as BS
import urllib2

class Command(NoArgsCommand):
    help = "Grab All Members Wikipedia Pages and Add them Into the DB"

    def handle_noargs(self, **options):        
        page = BS(urllib2.urlopen("http://data.openaustralia.org/members/wikipedia-commons.xml"))

        for member in page.findAll("personinfo"):
            m = member.objects.get(oa_id=member['id'])
            m.wikipedia = member['wikipedia_url']
            m.save()


