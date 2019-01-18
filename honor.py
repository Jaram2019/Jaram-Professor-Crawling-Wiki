from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

with urllib.request.urlopen("http://sw.hanyang.ac.kr/members/professor.php?ptype=list&code=professor&category=44") as response:
	html=response.read()
	soup=BeautifulSoup(html, 'html.parser')

name_kor=[]
name_eng=[]
email=[]

for x in soup.find_all("td", class_="organ_list"):
	name_kor.append(x.find("td", class_="or_name").string)
	for th in x.find_all("th", class_="or_tit"):
		if th.string=="영문명":
			name_eng.append(th.next_sibling.next_sibling.string)
		elif th.string=="이메일":
			email.append(th.next_sibling.next_sibling.find('a')['href'])

	return name_kor, name_eng, email