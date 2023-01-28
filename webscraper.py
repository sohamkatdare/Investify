import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By


def investopedia_search(searchquery):
    searchquery = '+'.join(searchquery.split())

    url = f'https://investopedia.com/search?q={searchquery}'
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver.implicitly_wapython webscraper.pit(30)
    # driver.get(url)

    # anchor = driver.find_element(By.ID, "search-results__link_1-0")
    # link = anchor.get_attribute('href')
    # driver.close()
    # return link

def investopedia_web_scrape(searchquery):
    article = ''

    searchList = str(searchquery).split()
    searchquery = ''
    for i in searchList:
        searchquery = searchquery + i + '+'

    url = f'https://investopedia.com/search?q={searchquery}'
    soup = bs(requests.get(url).content, 'html.parser')

    anchor = soup.find(id='search-results__link_1-0')
    link = anchor['href']

    # driver = webdriver.Firefox()
    # driver.implicitly_wait(30)
    # driver.get(url)

    # anchor = driver.find_element_by_id("search=results__link_1-0")
    # anchor.click()
    # link = driver.getCurrentUrl()

    soup = bs(requests.get(link).content, 'html.parser')
    for o in soup.find(id='mntl-sc-page_1-0').find_all('p', recursive=False):
        if len(o.text) > 20:
            article += o.text + ' '
    
    return article

# if __name__ == '__main__':
#     # print(investopedia_search('Altman Z Score'))
#     print(investopedia_web_scrape(investopedia_search('Altman Z Score')))

# print(investopedia_web_scrape('bollinger bands'))
# print(investopedia_web_scrape('worden stochatics'))
# print(investopedia_web_scrape('macd'))
# print(investopedia_web_scrape('On-Balance-volume'))
# print(investopedia_web_scrape('parabolic stop and reverse'))
# print(investopedia_web_scrape('relative strength index'))
# print(investopedia_web_scrape('commodity channel index how to calculate'))
# print(investopedia_web_scrape('chaikin oscillator'))