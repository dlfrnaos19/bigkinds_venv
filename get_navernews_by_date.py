# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import requests

def get_naver_news_soup(start_day="2022.07.15", end_day="2022.07.15", keyword="아이유"):
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
    
    news_element = soup.select('#main_pack > section > div > div.group_news > ul > li > div > div > a')
    title_list = []
    link_list = []
    for i in news_element:
        title_list.append(i.text)
        link_list.append(i.get('href'))
    
    related_soup = soup.select('#nx_right_related_keywords > div > div.related_srch > ul > li')
    if related_soup == []:
        print('no related keywords')
        return title_list, link_list
    else:
        rel_keyword_list = []
        for i in soup.select('#nx_right_related_keywords > div > div.related_srch > ul > li'):
            rel_keyword_list.append(i.text)
        return title_list, link_list, rel_keyword_list
    
if "__main__" == __name__:
    # 연관검색어가  있을 경우, 연관검색까지 3개의 리스트 튜플로 반환 (뉴스타이틀, 뉴스링크, 연관검색어)
    # 연관검색어가 없으면 2개의 튜플 리스트로 반환 (뉴스타이틀, 뉴스링크)
    result = get_naver_news_soup("2022.05.13", "2022.05.13", "마리화나")

# %%
result


