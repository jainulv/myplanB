#!/usr/bin/env python3

'''
scrape_course_cat.py: Scrapes courses provided by all departments mentioned on the
website https://www.washington.edu/students/crscat/ and saves the data in a JSON file.

__author__='Jainul Vaghasia'
__email__='jnv3@uw.edu'
__status__='Development'
'''
# Last edited by: Akshit Patel, reason: changed the single quotes to double quotes.

# standard imports
import json                       # for dumping json into a file
import io                         # for file input/ouput

# libraries for scraping
import urllib.request             # for establishing the connection to the web
from bs4 import BeautifulSoup     # for getting HTML of a page and parsing it

# libraries for optimization
import concurrent.futures         # for async connection

# global variables
dept_dict={}                      # contains department name for each page in dept_list
all_list=[]                      # list of dictionaries of department name and courses
base_url='https://www.washington.edu/students/crscat/'  # starting URL

def open(url):
    '''
    Opens the connection to the given url and returns the linked Soup object.

    Parameters
    ----------
    url: String
        URL of the page to which the connection needs to be established

    Return values
    -------------
        Returns a Soup object linked to the given URL if the connection is successful
    '''
    with urllib.request.urlopen(url) as url:
        response=url.read()
        return BeautifulSoup(response, 'html5lib')

def a_scrape(elem):
    '''
    Extracts the link address and text from the given link element.

    Parameters
    ----------
    elem: Tag
        The link element that needs to be extracted as described above
    '''
    for j in elem.find_all('a'):
        # filter cases of links that link to the a section of the current page itself
        if '.html' in j['href']:
            # filter duplicate links
            if j['href'] not in dept_dict.keys():
                # add the link and the department name
                dept_dict[j['href']]=j.getText()

def scrape_for_depts(url):
    '''
    Scrapes the given url of a page that is similar in structure to the base_url page
    to generate the list of all departments and their names.

    Parameters
    ----------
    url: String
        URL of the page described above
    '''
    # establish the connection
    soup=open(url)
    # find all ul elements as the departments are all HTML lists
    all_ul_elems=soup.find_all('ul')
    for uls in all_ul_elems:
        # filter classed elements
        if not uls.has_attr('class'):
            # find all li elements and a_scrape them for level 2 and 3 lists
            li_elems=uls.find_all('li')
            for x in li_elems:
                # find all ul elements if present and a_scrape them
                ul_elems=x.find_all('ul')
                for y in ul_elems:
                    a_scrape(y)
                a_scrape(x)

def scrape_for_courses(url, code):
    '''
    Scrapes the course page linked to the given url and structures them like JSON.

    Parameters
    ----------
    url: String
        URL of the page described above

    code: String
        Tail of the page URL
    '''
    soup=open(url)
    cname=dept_dict[code]
    # add the department name
    course_dict={"cname":cname.strip('\n')}
    c_list=[]
    all_a_elems=soup.find_all('a')
    for uls in all_a_elems:
        # filter all empty link elements and non-course link elements
        if uls.has_attr('name') and uls.findChildren():
            # add course title
            temp_dict={"title":uls.find('b').getText()}
            # add course description if available, N/A otherwise
            if uls.findChildren() and len(uls.find_all('br'))>1:
                temp_dict["description"]=str(uls.select('br')[0].next_sibling)
            else:
                temp_dict["description"]="N/A"
            c_list.append(temp_dict)
    # append the new courses to previously added courses
    course_dict["courses"]=c_list
    all_list.append(course_dict)

def write_JSON(dict):
    '''
    Dumps the given dictionary to a JSON file named courses.json.
    
    Parameters
    ----------
    dict: Dictionary
       The dictionary that needs to be written
    '''
    with io.open('courses.json','w') as fout:
        json.dump(dict,fout)

def main():
    '''
    Main method for the script
    '''
    scrape_for_depts(base_url)
    print('Number of departments on website:', len(dept_dict.keys()))
    # asynchronous scraping with 24 max_workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
        future_results={executor.submit(scrape_for_courses, base_url+i, i):
                                i for i in dept_dict.keys()}

    write_JSON({"catlog":all_list})
    print('Number of departments in JSON file: ', len(all_list))
    print('Done!')
        
if __name__=='__main__':
    main()
