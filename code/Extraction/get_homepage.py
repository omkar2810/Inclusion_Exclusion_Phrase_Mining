## Get TripAdvisor home page of a tourist site

from bs4 import BeautifulSoup 
from selenium import webdriver
import pandas as pd
import time
import os
import pickle
import re

curpath = os.path.abspath(os.curdir)

## CSV containing the list of all the homepage urls of sites
df = pd.read_csv('popular_sites.csv')

driver = webdriver.Chrome(executable_path='./chromedriver')

for i in range(len(df)):
    ext = "+".join(df.iloc[i]['Name'].split(' '))
    ext += '+tripadvisor'
    driver.get("https://www.google.com/search?q="+ext)

    try:
        results = driver.find_elements_by_css_selector('div.g')
        href = ""
        i = 0
        while 'attraction' not in href.lower():
            link = results[i].find_element_by_tag_name("a")
            href = link.get_attribute("href")
            df.iloc[i]['url'] = href.split('/')[-1]
            i += 1
    except:
        err.append(row['Name'])