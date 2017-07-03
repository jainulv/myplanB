#!/usr/bin/env python3

from bs4 import BeautifulSoup
<<<<<<< HEAD
import urllib.request
import pandas as pd

dict={}
=======
from bs4 import SoupStrainer
import urllib.request
import pandas as pd
import json
import io
import time
import concurrent.futures

dept_dict={}
course_dict={}

def open(url, tag=None, lxml=False):
    with urllib.request.urlopen(url) as url:
        r=url.read()
        soup=None
        if tag:
            only_tags=SoupStrainer(tag)
            soup=BeautifulSoup(r, 'html.parser', parse_only=only_tags)
        elif not lxml:
            soup=BeautifulSoup(r, 'html5lib')
        else:
            soup=BeautifulSoup(r, 'lxml')
        return soup
>>>>>>> 582660d4c6c36b73b0b27c7a7326b1e9c8dbdfe6

def a_scrape(elem):
    for j in elem.find_all('a'):
        if '.html' in j['href']:
<<<<<<< HEAD
            dict[j.getText()]=j['href']
    
def scrape(url):
    with urllib.request.urlopen(url) as url:
        r=url.read()
        soup=BeautifulSoup(r, 'html5lib')
        for uls in soup.find_all('ul'):
            if not uls.has_attr('class'):
                for x in uls.find_all('li'):
                    for y in x.find_all('ul'):
                        a_scrape(y)
                    a_scrape(x)

scrape('https://www.washington.edu/students/crscat/')
print(dict)
=======
            dept_dict[j.getText()]=j['href']

def scrape(url):
    soup=open(url)
    all_ul_elems=soup.find_all('ul')
    for uls in all_ul_elems:
        if not uls.has_attr('class'):
            li_elems=uls.find_all('li')
            for x in li_elems:
                ul_elems=x.find_all('ul')
                for y in ul_elems:
                    a_scrape(y)
                a_scrape(x)

def scrape_courses(url):
    soup=open(url, 'a')
    for uls in soup:
        if uls.has_attr('name'):
            if uls.findChildren() and len(uls.find_all('br'))>1:
                course_dict[uls.find('b').getText()]=str(uls.select('br')[0].next_sibling)
            else:
                course_dict[uls.find('b').getText()]='N/A'

def normalize():
    json_data=[]
    for k,v in course_dict.items():
        json_data.append({'title':k,'info':v})
    return json_data

t0=time.time()
base_url='https://www.washington.edu/students/crscat/'
scrape(base_url)
print('Number of departments: ', len(dept_dict))

URLS=(base_url+i for i in dept_dict.values())
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    future_results={executor.submit(scrape_courses, url): url for url in URLS}

with io.open('../myplanB/courses.json','w') as fout:
    json.dump(normalize(), fout)
print('Done!')
print('Number of courses: ', len(course_dict))

t1=time.time()
total_time=t1-t0
print('Time taken: ', total_time)

>>>>>>> 582660d4c6c36b73b0b27c7a7326b1e9c8dbdfe6
