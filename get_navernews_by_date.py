from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import requests

def get_naver_news_soup(start_day, end_day, keyword):
    params = {
    'sm': 'tab_hty.top',
'where': 'news',
'query': str(keyword),
'oquery': str(keyword),
'tqi': 'hWiWBwprvxsssNYIuRZssssstwZ-398548',
'nso': 'so:r,p:from20220610to20220610',
'de': str(end_day),  # yyyy.mm.dd
'ds': str(start_day),
'mynews': '0',
'office_section_code': '0',
'office_type': '0',
'pd': '3',
'photo': '0',
'sort': '0',
}
    
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'
    }
    url = "https://search.naver.com/search.naver"
    res = requests.get(url, params=params,headers=header)
    if res.status_code == 200:
        soup = bs(res.content,'lxml')
    else:
        print('something went wrong')
        print(res.status_code)
        return None
    return soup

if "__main__" == __name__:
    soup = get_naver_news_soup("2022.07.10", "2022.07.10", "삼성전자")
    print(soup)
    