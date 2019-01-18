from bs4 import BeautifulSoup
import urllib.request
import urllib.parse


def get_adjunct():
    with urllib.request.urlopen(
            "http://sw.hanyang.ac.kr/members/professor.php?ptype=list&code=professor&category=53") as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

    photo = []
    name_kor = []
    name_eng = []
    position = []
    email = []

    for x in soup.find_all("td", class_="organ_list"):
        name_kor.append(x.find("td", class_="or_name").string)
        photo.append(x.find("img")["src"])
        for th in x.find_all("th", class_="or_tit"):
            if th.string == "영문명":
                name_eng.append(th.next_sibling.next_sibling.string)
            elif th.string == "직위":
                position.append(th.next_sibling.next_sibling.string)
            elif th.string == "이메일":
                email.append(th.next_sibling.next_sibling.find('a')['href'])

        return photo, name_kor, name_eng, position, email


def get_honor():
    with urllib.request.urlopen(
            "http://sw.hanyang.ac.kr/members/professor.php?ptype=list&code=professor&category=44") as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

    photo = []
    name_kor = []
    name_eng = []
    email = []

    for x in soup.find_all("td", class_="organ_list"):
        name_kor.append(x.find("td", class_="or_name").string)
        photo.append(x.find("img")["src"])
        for th in x.find_all("th", class_="or_tit"):
            if th.string == "영문명":
                name_eng.append(th.next_sibling.next_sibling.string)
            elif th.string == "이메일":
                email.append(th.next_sibling.next_sibling.find('a')['href'])

        return photo, name_kor, name_eng, email


def get_prof():
    with urllib.request.urlopen(
            "http://sw.hanyang.ac.kr/members/professor.php?ptype=list&code=professor&category=43") as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

    photo = []
    name_kor = []
    name_eng = []
    position = []
    location = []
    email = []

    for x in soup.find_all("td", class_="organ_list"):
        name_kor.append(x.find("td", class_="or_name").string)
        photo.append(x.find("img")["src"])
        for th in x.find_all("th", class_="or_tit"):
            if th.string == "영문명":
                name_eng.append(th.next_sibling.next_sibling.string)
            elif th.string == "직위":
                position.append(th.next_sibling.next_sibling.string)
            elif th.string == "위치":
                location.append(th.next_sibling.next_sibling.string)
            elif th.string == "이메일":
                email.append(th.next_sibling.next_sibling.find('a')['href'])

    return photo, name_kor, name_eng, position, location, email
