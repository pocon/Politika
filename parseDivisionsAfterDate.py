import BeautifulSoup,urllib2,re,datetime

# Get the .xml hansard transcripts as a chronological list from http://data.openaustralia.org/scrapedxml/representatives_debates/

links=[]
temp=urllib2.urlopen(urllib2.Request("http://data.openaustralia.org/scrapedxml/representatives_debates/")).read()
index=BeautifulSoup.BeautifulSoup(temp)
for linkTag in index.findAll("a"):
	links.append(str(linkTag["href"]))
links=links[5:]

''' getDivisions(date) retrieves all the votes on motions from the Hansard transcript of the given sitting date. Is only used internally, external interface is to use getDivisionsAfter(date).
Notes:
Accepts: a date object, which must exactly be analogous to a date represented by a string in links (getDivisions will convert to yyyy-mm-dd)
Returns a list "day", day=[master,master,master...]
Each master is a list representing a single division with:
 master[0]=list containing the id strings of the ayes votes, defined by the regex ^uk\.org\.publicwhip/member/[0-9]+$
 master[1]=list containing the id strings of the noes votes, ""
 master[2]=string containing the motion/question that triggered the division
 master[3]=date/time object representing when master[2] occurred
 master[4]=url link to aph hansard
 Nothing is done with pairs
'''

def getDivisions(date):
	year=date.year
	month=date.month
	if month<10:month=str("0"+str(month))
	day=date.day
	if day<10:day=str("0"+str(day))
	dateAsString=str(year)+"-"+str(month)+"-"+str(day)+".xml" # Ensures months and days are at least 2 digits long
	divisionsForDate=[]
	if dateAsString in links:
		rawHansard=urllib2.urlopen(urllib2.Request("http://data.openaustralia.org/scrapedxml/representatives_debates/"+dateAsString)).read()
		procHansard=BeautifulSoup.BeautifulSoup(rawHansard)
		for division in procHansard.findAll("division"): # Parse each <division>
			master=[]
			master.append([])
			master.append([])
			master.append("")
			master.append(date)
			master.append("")
			members=division.findAll("member")
			for member in members:
				if member.parent.name=="memberlist": # Ignore <member>s within <pair></pair>
					if member["vote"]=="aye":master[0].append(str(member["id"]))
					else:master[1].append(str(member["id"]))# Assuming all votes are either "aye" or "no" and there are no errors in the xml
			if division.findPreviousSibling().name=="speech": # assuming the reason for division is given in the <p> childs of the first <speech> tag before the <division> tag
				for pTag in division.findPreviousSibling().findAll("p"):
					if pTag.string!=None:master[2]+=str(pTag.string)
			master[4]=str(division["url"])
			divisionsForDate.append(master)
	else:
		raise ValueError,"No transcripts for that date"
	return divisionsForDate


'''getDivisionsAfter(date) accepts a date object and returns a list of division lists, which are defined according to master, representing all divisions on or after that date
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
			final+=getDivisions(cdate)
		else:
			if cdate.year>=date.year:
				if cdate.month>=date.month:
					if cdate.day>=date.day:
						reachedDate=True
						final+=getDivisions(cdate)
	return final
