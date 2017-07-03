#!/usr/bin/env python3

from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import urllib.request
import pandas as pd
import json
import io
import time
import concurrent.futures

dept_list=[]
dept_dict={}
all_list=[]

def open(url):
    with urllib.request.urlopen(url) as url:
        r=url.read()
        return BeautifulSoup(r, 'html5lib')

def a_scrape(elem):
    for j in elem.find_all('a'):
        if '.html' in j['href']:
            if j['href'] not in dept_list:
                dept_list.append(j['href'])
                dept_dict[j['href']]=j.getText()

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

def scrape_courses(url, code):
    soup=open(url)
    cname=str(soup.find('h1').select('br')[len(soup.find('h1').find_all('br'))-1].next_sibling)
    cname=dept_dict[code]
    course_dict={'cname':cname.strip('\n')}
    c_list=[]
    all_a_elems=soup.find_all('a')
    for uls in all_a_elems:
        if uls.has_attr('name') and uls.findChildren():
            temp_dict={'title':uls.find('b').getText()}
            if uls.findChildren() and len(uls.find_all('br'))>1:
                temp_dict['description']=str(uls.select('br')[0].next_sibling)
            else:
                temp_dict['description']='N/A'
            c_list.append(temp_dict)
    course_dict['courses']=c_list
    all_list.append(course_dict)

def write_JSON(dict):
    with io.open('../myplanB/courses.json','w') as fout:
        json.dump(dict,fout)
    
t0=time.time()
base_url='https://www.washington.edu/students/crscat/'
scrape(base_url)
#dept_list=set(dept_list)
print('Number of departments: ', len(dept_list))
URLS=(base_url+i for i in dept_list)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    future_results={executor.submit(scrape_courses, base_url+i, i): i for i in dept_list}

write_JSON(all_list)
print('Number of departments in JSON file: ', len(all_list))
print('Done!')

t1=time.time()
total_time=t1-t0
print('Time taken: ', total_time)

