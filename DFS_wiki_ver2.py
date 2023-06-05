import requests
from bs4 import BeautifulSoup
import re
import time

def my_crawler(seed, keywords):
    start_time = time.time()  # 시작 시간 기록

    List_of_links = []
    parent_list = []
    child_list = []
    parent_list.append(seed)
    count = 1
    depth = 1
    x = 0
    while len(parent_list) < 1000 and x < len(parent_list):
        if depth >= 6:
            break
        List_of_links = go_crawl(parent_list[x], keywords)
        for i in List_of_links:
            if i not in child_list:
                child_list.append(i)
        for j in child_list:
            if j not in parent_list and len(parent_list) < 1000:
                parent_list.append(j)
                count = count + 1
        if len(child_list) == count:
            child_list = []
            depth = depth + 1
        x = x + 1

    number = 1
    with open('DSF_cralwing_ver2.txt', 'w') as f:
        for i in parent_list:
            row = str(number) + " " + str(i) + "\n"
            f.write(row)
            number += 1

    end_time = time.time()  # 종료 시간 기록
    elapsed_time = end_time - start_time  # 실행 시간 계산
    print("Execution time: {:.2f} seconds".format(elapsed_time))

def go_crawl(url, keywords):
    reExp = "^(" + "|".join(keywords) + ")| (" + "|".join(keywords) + ") |" + "_(" + "|".join(keywords) + ")_" 
    Exp = re.compile(reExp, re.IGNORECASE)
    wikistring = "https://en.wikipedia.org"
    totallinks, child_links = [], []
    time.sleep(1)
    seedinfo = requests.get(url)
    raw_data = seedinfo.text
    soup = BeautifulSoup(raw_data, 'html.parser')
    body_content = soup.find('div', {'id': 'mw-content-text'})
    
    if len(soup.find('div', {'class': 'thumbcaption'}) or ()) > 1:
        soup.find('div', {'class': 'thumbcaption'}).decompose()
        
    if len(soup.find('table', {'class': 'vertical-navbox nowraplinks hlist'}) or ()) > 1:
        soup.find('table', {'class': 'vertical-navbox nowraplinks hlist'}).decompose()
        
    if len(soup.find('table', {'class': 'vertical-navbox nowraplinks'}) or ()) > 1:
        soup.find('table', {'class': 'vertical-navbox nowraplinks'}).decompose()
        
    if len(soup.find('ol', class_='references') or ()) > 1:
        soup.find('ol', class_='references').decompose()

    for link in body_content.find_all('a', {'href': re.compile("^/wiki")}):
        urlString = link.get('href')
        len1 = len(Exp.findall(urlString))
        try:
            anchorTextString = link.text
        except UnicodeEncodeError as e:
            error = e
        len2 = len(Exp.findall(anchorTextString))
        if (len1 > 0) or (len2 > 0):
            if ':' not in link.get('href'):
                link_text = wikistring + link.get('href')
                refine_text = link_text.split('#')
                totallinks.append(str(refine_text[0]))
    
    for i in totallinks:
        if i not in child_links:
            if len(i) > 1:
                child_links.append(i)
    return child_links

keywords = input("Enter the Keywords (separated by comma): ").split(",")
my_crawler('https://en.wikipedia.org/wiki/SM_Entertainment', keywords)
Link_limit = 350
