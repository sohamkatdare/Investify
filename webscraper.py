import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By


def investopedia_search(searchquery):
    searchquery = '+'.join(searchquery.split())

    url = f'https://investopedia.com/search?q={searchquery}'
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    driver.implicitly_wait(30)
    driver.get(url)

    anchor = driver.find_element(By.ID, "search-results__link_1-0")
    link = anchor.get_attribute('href')
    driver.close()
    return link

def investopedia_web_scrape(link):
    soup = bs(requests.get(link).content, 'html.parser')

    article = ''
    for o in soup.select('p'):
        if len(o.text) > 20:
            article += o.text + ' '
    
    return article

if __name__ == '__main__':
    # print(investopedia_search('Altman Z Score'))
    print(investopedia_web_scrape(investopedia_search('Altman Z Score')))
