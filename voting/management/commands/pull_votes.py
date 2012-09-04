import BeautifulSoup,urllib2,re,datetime


"""
A management command which Grabs Electorates and their members from OA

"""

from django.core.management.base import NoArgsCommand
from members.models import *
from voting.models import *
from BeautifulSoup import BeautifulStoneSoup as BS
import urllib2

class Command(NoArgsCommand):
    help = "Grab All Electorates and Add them Into the DB with Member"

    def handle_noargs(self, **options):     
        links=[]
        temp=urllib2.urlopen(urllib2.Request("http://data.openaustralia.org/scrapedxml/representatives_debates/")).read()
        index=BeautifulSoup.BeautifulSoup(temp)
        for linkTag in index.findAll("a"):
            links.append(str(linkTag["href"]))
        links=links[5:] # Chop off links to things other than the relevant xmls

        '''
        getDivisions():
        Accepts: a date object, which must exactly be analogous to a date represented by a string in links (getDivisions will convert to yyyy-mm-dd)
        '''

        def getDivisions(date):
            year=date.year
            month=date.month
            if month<10:month=str("0"+str(month))
            day=date.day
            if day<10:day=str("0"+str(day))
            dateAsString=str(year)+"-"+str(month)+"-"+str(day)+".xml" # Ensures months and days are at least 2 digits long
            print dateAsString
            if dateAsString in links:
                rawHansard=urllib2.urlopen(urllib2.Request("http://data.openaustralia.org/scrapedxml/representatives_debates/"+dateAsString)).read()
                procHansard=BeautifulSoup.BeautifulSoup(rawHansard)
                for division in procHansard.findAll("division"): 
                    vote = Vote(url=str(division["url"]), date=date)
                    vote.save()
                    members=division.findAll("member")
                    for member in members:
                        if member.parent.name=="memberlist":
                            if member["vote"]=="aye":
                                vote.ayes.add(Member.objects.get(oa_id=member['id'])
                            else:
                                vote.noes.add(Member.objects.get(oa_id=member['id'])

                        elif member.parent.name=="pairs":
                            pairmembers=member.parent.findAll("member")
                            p = MemberPair(Member1=pairmembers[0]["id"], Member2=pairmembers[1]["id"])
                            p.save()
                            vote.pairs.add(MemberPair)
                        else:pass # do nothing with member tags not in a division
                    if division.findPreviousSibling().name=="speech": # assuming the reason for division is given in the <p> childs of the first <speech> tag before the <division> tag
                        reason=""
                        for pTag in division.findPreviousSibling().findAll("p"):
                            if pTag.string!=None:reason+=str(pTag.string)
                            
                        vote.motion = reason
 
            else:
                raise ValueError,"No transcripts for that date"


        '''getDivisionsAfter(date) accepts a date object and pulls all divisions after that date (NOT including that date)
        '''
        def getDivisionsAfter(date):
            final=[]
            templinks=[]
            reachedDate=False
            for edate in links:
                extractDate=re.compile(r"^([0-9]{4})\-([0-9]{2})\-([0-9]{2})\.xml$").search(edate) # Use regex grouping to get year, month and day info
                tempDate=datetime.date(int(extractDate.group(1)),int(extractDate.group(2)),int(extractDate.group(3)))
                templinks.append(tempDate) # convert links to a list of date objects
            for cdate in templinks: # Iterate through the dates until we reach the date we want, and parse all dates after that
                if reachedDate:
                    getDivisions(cdate)
                else:
                    if cdate.year>=date.year:
                        if cdate.month>=date.month:
                            if cdate.day>=date.day:
                                reachedDate=True
            writeNewDate=open("lastdatepulled.txt","w")
            writeNewDate.write(str(cdate.year)+"\n"+str(cdate.month)+"\n"+str(cdate.day))
            writeNewDate.close()

        try:
            rawpdate=open("lastdatepulled.txt","rU") #lastdatepulled.txt is the "counter", the last date that was pulled, a 3 line text file the first line the year, the second the month and the third the day
            datelimit=datetime.date(int(rawpdate.readline().rstrip()),int(rawpdate.readline().rstrip()),int(rawpdate.readlin(),rstrip()))
            rawpdate.close()
            getDivisionsAfter(datelimit)
        except IOError:
            getDivisionsAfter(datetime.date(2010,8,21)) #If lastdatepulled.txt does not exist or cannot be read, program will auto-pull all divisions after 21 August 2010, the last election

