import requests
from bs4 import BeautifulSoup

baseurl = 'https://docs.mongodb.org/manual/release-notes/'


# Get Major Release Version
def getReleases():
	releases=[]
	plain= requests.get(baseurl,verify=False).text
	soup = BeautifulSoup(plain,'lxml')
	c_release = soup.find(id ="current-stable-release").find("li").find("a")

	
	
	tmp = {'link':c_release.get('href'),'name':c_release.string}
	releases.append(tmp)
	
	p_release = soup.find(id ="previous-stable-releases").find_all("li")
	
	for p in p_release:
		rel = p.find("a")
		tmp = {'link':rel.get('href'),'name':rel.string}
		releases.append(tmp)
	
	
	return releases
	
# Get Minor Release Version
def getMinorReleases(url):
	plain = requests.get(baseurl+url,verify=False).text
	soup = BeautifulSoup(plain,'lxml')
	mreleases=[]
	minors= soup.find(id ="minor-releases").find_all(class_="section")
	
	for minor in minors:
		tmp={'info' : minor.find("h3").contents[0],'content':minor.find_all("li")}
		mreleases.append(tmp)
		
	return mreleases

releases = getReleases()

for release in releases:
	print getMinorReleases(release['link'])
