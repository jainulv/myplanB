#!/usr/bin/env python3

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

dict={}

def a_scrape(elem):
    for j in elem.find_all('a'):
        if '.html' in j['href']:
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
