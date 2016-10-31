# -*- coding: utf8 -*-

import requests
from bs4 import BeautifulSoup
import sys
import re
import time
from datetime import datetime,timedelta
import json,io

if len(sys.argv) !=4:
	print "usage : naver_news.py {start_date} {end_date} {query_text}"
	print "ex) naver.news.py 2016-10-01 2016-10-30 helloworld"
	exit()

query = sys.argv[3]

start_date = datetime.strptime(sys.argv[1],'%Y-%m-%d') - timedelta(days=1)
end_date = datetime.strptime(sys.argv[2],'%Y-%m-%d')

now = datetime.now()

lists=[]

while 1:
	start_date = start_date + timedelta(days=1)

	if start_date == end_date or start_date > now :
		break;
	
	date_str = start_date.strftime('%Y-%m-%d')

	baseurl = 'http://news.naver.com/main/search/search.nhn?query='+query+'&st=news.all&q_enc=EUC-KR&r_enc=UTF-8&r_format=xml&rp=none&sm=title.basic&ic=all&so=rel.dsc&detail=1&pd=4&r_cluster2_start=1&r_cluster2_display=10&start=1&display=10&startDate='+date_str+'&endDate='+date_str+'&dnaSo=rel.dsc&page='


	plain = requests.get(baseurl).text


	soup = BeautifulSoup(plain,'lxml')

	result_num = soup.find_all("span",class_="result_num")



	try: 
		# 1000건 이상시 1,000 으로 표현될때
		total_num = int(re.findall('\d,\d*',result_num[0].string)[0].replace(',',''))+1
	except:
		# 1000건 미만시 
		total_num = int(re.findall('\/\s*\d*',result_num[0].string)[0].split('/ ')[1])+1

	page_num = 1+ (total_num / 10)

	cnt=0
	for i in range(1,page_num+1):

		baseurl = 'http://news.naver.com/main/search/search.nhn?query='+query+'&st=news.all&q_enc=EUC-KR&r_enc=UTF-8&r_format=xml&rp=none&sm=title.basic&ic=all&so=rel.dsc&detail=1&pd=4&r_cluster2_start=1&r_cluster2_display=10&start=1&display=10&startDate='+date_str+'&endDate='+date_str+'&dnaSo=rel.dsc&page='+str(i)
		plain = requests.get(baseurl).text
		soup = BeautifulSoup(plain,'lxml')


		for list in soup.find_all("a",class_="tit"):
			tmp = {'link':list.get('href'),'title':list.string,'date':date_str}
			lists.append(tmp)
			#print tmp
			cnt+=1

		
		time.sleep(1)

	print 'total : '+str(cnt) + ' / date : '+date_str


with io.open('output.json','w',encoding='utf-8') as f:
	f.write(unicode(json.dumps(lists,ensure_ascii=False)))




