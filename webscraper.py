import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
# import numpy
# import pandas as pd
# import matplotlib.pyplot as plt

def investopediaScrape(searchquery): # Just get rid of the selenium and pass in a link.
    # Like try scraping this example. https://www.investopedia.com/terms/s/stockmarket.asp
    article = ''

    searchList = searchquery.split()
    searchquery = ''
    for i in searchList:
        searchquery = searchquery + i + '+'

    url = f'https://investopedia.com/search?q={searchquery}'
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.get(url)

    anchor = driver.find_element(By.ID, "search-results__link_1-0") 
    anchor.click()
    link = driver.current_url # it might be easier to just use the link directly. That gives more control to the user.

    soup = bs(requests.get(link).content, 'html.parser')

    for o in soup.select('#article-body div p'):
        article = article + '{}{}'.format(o.text) + "\n\n"
    
    return article

if __name__ == '__main__':
    print(investopediaScrape('stock market'))