"""
A management command which Grabs MPs Websites from OA

"""

from django.core.management.base import NoArgsCommand
from members.models import *
from BeautifulSoup import BeautifulStoneSoup as BS
import urllib2

class Command(NoArgsCommand):
    help = "Grab All Members Websites and Add them Into the DB"

    def handle_noargs(self, **options):        
        page = BS(urllib2.urlopen("http://data.openaustralia.org/members/websites.xml"))

        for member in page.findAll("personinfo"):
            m = Member.objects.get(oa_id=member['id'])
            m.website = member['mp_website']
            m.aph_page = member['mp_contactdetails']
            m.save()


