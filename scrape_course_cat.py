#!/usr/bin/env python3

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time

dept_dict={}
course_dict={}

def a_scrape(elem):
    for j in elem.find_all('a'):
        if '.html' in j['href']:
            dept_dict[j.getText()]=j['href']

def open(url):
    with urllib.request.urlopen(url) as url:
        r=url.read()
        return BeautifulSoup(r, 'html5lib')
        
def scrape(url):
    soup=open(url)
    for uls in soup.find_all('ul'):
        if not uls.has_attr('class'):
            for x in uls.find_all('li'):
                for y in x.find_all('ul'):
                    a_scrape(y)
                a_scrape(x)

def scrape_courses(url):
    soup=open(url)
    for uls in soup.find_all('a'):
        if uls.has_attr('name'):
            if uls.findChildren():
                course_dict[uls.find('b').getText()]=uls.select('br')[0].next_sibling

t0=time.time()
base_url='https://www.washington.edu/students/crscat/'
scrape(base_url)
for i in dept_dict.values():
    scrape_courses(base_url+i)
courses_pd=pd.DataFrame.from_dict(course_dict, orient='index')

print(courses_pd)
print('Done!')
print('Number of courses: ', len(course_dict))
t1=time.time()
total_time=t1-t0
print('Time taken: ', total_time)

