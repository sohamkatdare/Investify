import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
# import numpy
# import pandas as pd
# import matplotlib.pyplot as plt


def askGPT(searchquery):

    sentence = f"write a 4-paragraph article about the importance of {searchquery} in finding a good stock to invest in"
    url = "https://chat.openai.com/chat"
    page = bs(requests/get(url).content, 'html.parser')

    payload = {}

    for i in page.select('form[action="/chat/" input[value]'):
        payload[i['name']] = i['value']
    payload['UQ_txt'] = sentence
    
    page = bs(requests.post(url, data=payload).text, 'html.parser')
    for o in page.select('.markdown p'):
        print('{}{}'.format(a.text), "\n\n")

def investopediaScrape(searchquery):
    article = ''

    searchList = searchquery.split()
    searchquery = ''
    for i in searchList:
        searchquery = searchquery + i + '+'

    url = f'https://investopedia.com/search?q={searchquery}'
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(url)

    anchor = driver.find_element_by_id("search=results__link_1-0")
    anchor.click()
    link = driver.getCurrentUrl()

    soup = bs(requests/get(link).content, 'html.parser')

    for o in soup.select('#article-body div p'):
        article = article + '{}{}'.format(o.text) + "\n\n"
    
    return article