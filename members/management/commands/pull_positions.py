"""
A management command which Grabs MPs Positions from OA

"""

from django.core.management.base import NoArgsCommand
from members.models import *
from BeautifulSoup import BeautifulStoneSoup as BS
import urllib2

class Command(NoArgsCommand):
    help = "Grab All Members Positions and Add them Into the DB"

    def handle_noargs(self, **options):        
        page = BS(urllib2.urlopen("http://data.openaustralia.org/members/ministers.xml"))

        for office in page.findAll("moffice"):
            if office['todate'] == "9999-12-31": # How OA stores current positions
                m = Member.objects.get(oa_matchid=member['matchid'])
                m.position = office['position']
                m.save()


