import requests
from bs4 import BeautifulSoup as bs
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