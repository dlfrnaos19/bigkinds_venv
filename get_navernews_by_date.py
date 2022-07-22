from bs4 import BeautifulSoup as bs
import requests
from tqdm import tqdm
import pandas as pd
import argparse

# 연관검색어가  있을 경우, 연관검색까지 3개의 리스트 튜플로 반환 (뉴스타이틀, 뉴스링크, 연관검색어)
# 연관검색어가 없으면 2개의 튜플 리스트로 반환 (뉴스타이틀, 뉴스링크)

parser = argparse.ArgumentParser()
parser.add_argument('--start_day', type=str, default='20220715', help='start day')
parser.add_argument('--end_day', type=str, default='20220715', help='end day')
parser.add_argument('--keyword', type=str, default='아이유', help='keyword')

def get_naver_news_soup(start_day="20220715", end_day="20220715", keyword="아이유"):
    
    """_summary_

    날짜는 겹칠 수 있습니다.
    
    Args:
        start_day (str): _description_. Defaults to "20220715".
        end_day (str): _description_. Defaults to "20220715".
        keyword (str): _description_. Defaults to "아이유".
    """
    
    
    date_list = pd.date_range(str(start_day), str(end_day), freq='D').to_pydatetime().tolist()
    target_date = [i.strftime('%Y.%m.%d') for i in tqdm(date_list, desc='convert week list to date')]
    
    
    params = {
    'sm': 'tab_hty.top',
'where': 'news',
'query': str(keyword),
'oquery': str(keyword),
'tqi': 'hWiWBwprvxsssNYIuRZssssstwZ-398548',
'nso': 'so:r,p:from20220610to20220610',
'de': target_date[-1],  # yyyy.mm.dd
'ds': target_date[0],
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
        result_dict = dict(
            title_list=title_list,
            link_list=link_list
        )
        df = pd.DataFrame(result_dict)
        df.to_csv('{}_{}_{}.csv'.format(keyword, start_day, end_day), index=False)
        return df
    else:
        rel_keyword_list = []
        for i in soup.select('#nx_right_related_keywords > div > div.related_srch > ul > li'):
            rel_keyword_list.append(i.text)
        
        result_dict = dict(
            title_list=title_list,
            link_list=link_list,
            rel_keyword_list=rel_keyword_list
        )
        df = pd.DataFrame(result_dict)
        df.to_csv('{}_{}_{}.csv'.format(keyword, start_day, end_day), index=False)
        return df
    
if "__main__" == __name__:
    args = parser.parse_args()
    result = get_naver_news_soup(args.start_day, args.end_day, args.keyword)


