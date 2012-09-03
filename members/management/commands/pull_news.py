"""
A management command which grabs 2007 ABC election websites on individual electorates.

"""

from django.core.management.base import NoArgsCommand
from members.models import *
from BeautifulSoup import BeautifulStoneSoup as BS
import urllib2
import datetime.datetime

class Command(NoArgsCommand):
    help = "Grab all electorates' websites for the 2007 election and add them into the DB"

    def handle_noargs(self, **options):        
        for member in Members.objects.all():
            adjustedName = member.full_name.replace(' ', '+')
            page = BS(urllib2.urlopen("http://news.google.com/news?q=%s&output=rss" % adjustedName))
            
            newsmp = MPNews(link1=page.findAll('link', limit=1))
                        
            for item in page.findAll('item'):
                itemDate = item['pubDate'].split(' ')
                if itemDate[2] == 'Jan':
                    pubMonth = 1
                elif itemDate[2] == 'Feb':
                    pubMonth = 2
                elif itemDate[2] == 'Mar':
                    pubMonth = 3
                elif itemDate[2] == 'Apr':
                    pubMonth = 4
                elif itemDate[2] == 'May':
                    pubMonth = 5
                elif itemDate[2] == 'Jun':
                    pubMonth = 6
                elif itemDate[2] == 'Jul':
                    pubMonth = 7
                elif itemDate[2] == 'Aug':
                    pubMonth = 8
                elif itemDate[2] == 'Sep':
                    pubMonth = 9
                elif itemDate[2] == 'Oct':
                    pubMonth = 10
                elif itemDate[2] == 'Nov':
                    pubMonth = 11
                elif itemDate[2] == 'Dec':
                    pubMonth = 12
                pubTime = itemDate[4].split(':')
                
                newarticle = MPNewsArticle(
                    title=item['title'],
                    link=item['link']
                    description=item['description']
                    pubDate=datetime.datetime(
                        int(itemDate[3]),
                        pubMonth,
                        int(itemDate[1]),
                        int(pubTime[0]),
                        int(pubTime[1]),
                        int(pubTime[2]) #GMT though
                    )
                newarticle.save()
                    
                newsmp.articles.add(newarticle)
            
            newsmp.save()
            
            member.news.add(newsmp)
            member.save()