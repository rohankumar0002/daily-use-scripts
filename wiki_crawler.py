# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 09:24:59 2019

@author: Rohan
"""

import os
from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd
import traceback
import json
from tqdm import tqdm
# os.mkdir('/home/achyutas/wiki')
#os.chdir('/home/achyutas/wiki')

try:
    TOPICS = []
    with open('topics.json', 'r') as f:
        TOPICS = json.load(f)
except:
    TOPICS = []
URL = 'https://en.wikipedia.org'


def get_page(url, callback):
    try:
        res = get(url)
        html = res.text
        soup = BeautifulSoup(html, features='lxml')
        links = [i.get('href') for i in soup.findAll('a', attrs={'href': re.compile("^/[\w]+")}) if i.get('href')]
        for script in soup(["script", "style"]):
            script.decompose()


        text = soup.get_text().encode('utf-8').decode()
#         print(text)
        name = res.url.split('/')[-1]
        if not os.path.exists(name):
            os.mkdir(name)
        with open(name + '/' +name + '.txt', 'w') as f:
            f.write(text.strip())
        try:
            df_list = pd.read_html(html.encode('utf-8').decode())
            for n, i in enumerate(df_list):
                if i.shape[0] > 5:
                    i.to_csv(name + '/' + str(n) + '.csv')
        except:
            pass
        TOPICS.append(name)
        return links
    except KeyboardInterrupt:
        with open('topics.json', 'w') as f:
            json.dump(TOPICS, f)
        with open('links.json', 'w') as f:
            json.dump(callback, f)
            quit()
    except:
        print(traceback.format_exc())
        return []


# R_LINK = []
def crawler(links):
    try:
        R_LINK = []
    #     links = get_page(url)
        for i in tqdm(links):
            if i.split('/')[-1] not in TOPICS:
                R_LINK.extend(get_page(URL+i, links))
#    temp = R_LINK.copy()
    except KeyboardInterrupt:
        with open('topics.json', 'w') as f:
            json.dump(TOPICS, f)
        with open('links.json', 'w') as f:
            json.dump(links, f)
            quit()
    return crawler(R_LINK)

if __name__ == '__main__':
    try:
        with open('links.json', 'r') as f:
            links = json.load(f)
    except:
        links = get_page(URL, [])
    crawler(links)
