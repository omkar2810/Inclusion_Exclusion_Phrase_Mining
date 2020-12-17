## Extract other review pages of a site from its homepage

from bs4 import BeautifulSoup 
from selenium import webdriver
import pandas as pd
import time
import os
import pickle
import re

curpath = os.path.abspath(os.curdir)

## CSV containing the list of all the homepage urls of sites
sites = pd.read_csv('popular_sites.csv')
urls = list(sites['URL'])

driver = webdriver.Chrome(executable_path='./chromedriver')


def download_page(cur_page,page_no,driver):
    driver.get(cur_page)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    links = soup.findAll('a',attrs={'class':'pageNum '},href=True)
    next_page = ""
    for link in links:
        if link.text == str(page_no + 1):
            next_page = link['href']
    
    cur_page = cur_page.split('/')[-1]
    with open('./data/'+cur_page,'w+') as fil:
        fil.write(driver.page_source)

    return 'https://www.tripadvisor.in' + next_page

for url in urls:
    num = 10
    url = re.sub('or[0-9]+-','',url)
    cur_page = 'https://www.tripadvisor.in/' + url
    for no in range(1,num+1):
        print(no)
        print(cur_page)
        cur_page = download_page(cur_page,no,driver)
    break