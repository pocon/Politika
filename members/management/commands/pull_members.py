"""
A management command which Grabs MPs from APH or updates them (note: if a member is removed, they will NOT be removed)

"""

from django.core.management.base import NoArgsCommand
from members.models import *
from django.conf import settings
import urllib2
from BeautifulSoup import BeautifulSoup as bs

class Command(NoArgsCommand):
    help = "Grab All Members and Add them Into the DB"

    def handle_noargs(self, **options):        
        def scrape_mps(page):
            p = bs(page)
            for MP in p.findAll('p', {'class': 'title'})[1:]:
                # Setup Member, Grab Files and Other boring stuff
                try:
                    member = Member.objects.get(profile_full_url = "http://www.aph.gov.au" + MP.find('a')['href'])
                except Member.DoesNotExist:
                    member = Member()
                member.profile_full_url = "http://www.aph.gov.au" + MP.find('a')['href']
                member.mpid = MP.find('a')['href'][-3:]
                mpage = urllib2.urlopen(member.profile_full_url)
                m_bs = bs(mpage)

                # Grab Name of Member
                member.full_name = m_bs.find('h1').string
                member.name = m_bs.find('h1').string.split(' ')[-3] + ' ' +  m_bs.find('h1').string.split(' ')[-2]

                # For Grabbing Voting Records
                member.vote_name = m_bs.find('h1').string.split(' ')[-2] + ', ' + m_bs.find('h1').string.split(' ')[-3][0]

                # Grab Electorate
                e = Electorate(electorate = m_bs.find('h2').string[11:].split(',')[0], state = m_bs.find('h2').string[11:].split(',')[1])
                e.save()
                member.electorate = e

                # Grab Positions and Party
                inserting_to = ''
                primary = False # Means that first listed position (on APH) is their 'Primary' Position, or most important position
                member.save() # Need a Primary Key for the Many-To-Many Below
                for tag in m_bs.find('div', {'class': 'col-half'}).dl.findAll():
                    if tag.string == 'Positions':
                        inserting_to = tag.string
                        primary = True
                    elif tag.string == 'Party':
                        inserting_to = tag.string
                    elif tag.string == 'Chamber':
                        inserting_to = tag.string

                    else:
                        if inserting_to == 'Positions':
                            n = Position(position=tag.string, primary=primary)
                            n.save()
                            member.positions.add(n)
                            primary = False

                        elif inserting_to == 'Party':
                            party, success = Party.objects.get_or_create(name = tag.string)
                            member.party = party

                member.url = "http://www.aph.gov.au" + m_bs.find('div', {'class': 'col-third col-last'}).p.a['href']
                member.image = m_bs.find('p', {'class': 'thumbnail'}).img['src']
                member.save()

        
        scrape_mps(urllib2.urlopen("http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?expand=1&q=&mem=1&par=-1&gen=0&ps=100&st=1"))
        scrape_mps(urllib2.urlopen("http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?page=2&expand=1&q=&mem=1&par=-1&gen=0&ps=100&st=1"))

        print "Done Adding MPs"
        
