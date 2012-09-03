import BeautifulSoup,urllib2,re
memberid={}
for member in BeautifulSoup.BeautifulSoup(urllib2.urlopen(urllib2.Request("http://data.openaustralia.org/members/divisions.xml")).read()).findAll("division"):
 memberid[int(re.compile(r"^uk\.org\.publicwhip/cons/([0-9]+)$").search(member["id"]).group(1))]=str(BeautifulSoup.BeautifulSoup(str(member)).findAll("name")[0]["text"])
