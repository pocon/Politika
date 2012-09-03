"""
A management command which grabs 2007 ABC election websites on individual electorates.

"""

from django.core.management.base import NoArgsCommand
from members.models import *
from BeautifulSoup import BeautifulStoneSoup as BS
import urllib2

class Command(NoArgsCommand):
    help = "Grab all electorates' websites for the 2007 election and add them into the DB"

    def handle_noargs(self, **options):        
        page = BS(urllib2.urlopen("http://data.openaustralia.org/members/links-abc-election.xml"))

        for consinfo in page.findAll("consinfo"):
            elec = Electorate.objects.get(electorate__iexact=consinfo['canonical'])
            elec.abc = consinfo['abc_election_results_2007']
            elec.save()
