import requests
from bs4 import BeautifulSoup
import re
import time

def my_crawler(seed):
    start_time = time.time()  # 시작 시간 기록

    List_of_links = []
    parent_list = []
    child_list = []
    parent_list.append(seed)
    count = 1
    depth = 1
    x = 0
    while len(parent_list) < 1000 and x < len(parent_list):
        if depth >= 7:
            break
        List_of_links = go_crawl(parent_list[x])
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
    with open('BFS_crawling_ver1.txt', 'w') as f:
        for i in parent_list:
            row = str(number) + " " + str(i) + "\n"
            f.write(row)
            number += 1

    end_time = time.time()  # 종료 시간 기록
    elapsed_time = end_time - start_time  # 실행 시간 계산
    print("Execution time: {:.2f} seconds".format(elapsed_time))

def go_crawl(url):
    time.sleep(1)
    wikistring = "https://en.wikipedia.org"
    totallinks, child_links = [], []
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
        if ':' not in link.get('href'):
            link_text = wikistring + link.get('href')
            refine_text = link_text.split('#')
            totallinks.append(str(refine_text[0]))
            
    for i in totallinks:
        if i not in child_links:
            if len(i) > 1:
                child_links.append(i)
    
    return child_links

my_crawler('https://en.wikipedia.org/wiki/SM_Entertainment')
