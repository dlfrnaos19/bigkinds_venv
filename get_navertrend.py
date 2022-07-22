# %%
import requests
import secrets
import pandas as pd
import argparse
import plotly.express as px

parser = argparse.ArgumentParser()
parser.add_argument('--sector', type=str, default="마리화나")
parser.add_argument('--keywords', type=str, default='메디콕스,마이더스AI,아이큐어')
parser.add_argument('--start_day', type=str, default='20220711')
parser.add_argument('--end_day', type=str, default='20220715')

def get_trend(sectors="마리화나", keywords="메디콕스,마이더스AI,아이큐어", start_date="20220611", end_date="20220715"):
    
    random_hash = 'N_'+secrets.token_hex(nbytes=16)
    url = 'https://datalab.naver.com/qcHash.naver'
    payload = {
    'queryGroups': f'{sectors}__SZLIG__'+ keywords,
'startDate': start_date,
'endDate': end_date,
'timeUnit': 'date',
'gender':'' ,
'age': '',
'device':'', 
}
    headers = {
    'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
'origin': 'https://datalab.naver.com',
'referer': 'https://datalab.naver.com/keyword/trendResult.naver?hashKey='+random_hash,
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'sec-gpc': '1',
}
    res = requests.post(url, data=payload,headers=headers)
    if res.status_code == 200:
        print('has 값 획득 성공')
        hash_key = res.json()['hashKey']
    else:
        print('hash 값 획득 실패')
        print(res.status_code, res.text)
    
    dataurl = 'https://datalab.naver.com/qcExcel.naver'
    params = {
    'hashKey': hash_key,
}
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'
}
    res = requests.get(dataurl, params=params, headers=headers)
    if res.status_code == 200:
        print('excel 파일 획득 성공')
        df = pd.read_excel(res.content, )
    else:
        print('excel 파일 획득 실패')
    
    date_dict = dict(
        dates=df.iloc[6:].values[:,0],
        search_num=list(df.iloc[6:].values[:,1].astype(float))
    )
    df = pd.DataFrame(date_dict)
    df.dates = pd.to_datetime(df.dates)
    df['trend_average'] = df.search_num.apply(lambda x: x - df.search_num.mean())
    
    fig = px.bar(df, x='dates',y='search_num',title=f'{sectors} 네이버 검색어 트렌드',color='trend_average')
    fig.update_layout(bargap=0.1)
    fig.update_layout(xaxis_title='날짜',yaxis_title='검색수',
                  title=dict(
                      xanchor='center',x=0.5
                  ))
    fig.update_layout(
    font=dict(
        family="Nanum Gothic",
        size=14,
        color="white",
    )
)
    fig.update_layout(paper_bgcolor='black',plot_bgcolor='black')
    fig.update_layout(xaxis=dict(
    tickformat='%y.%m.%d',
))
    fig.layout.coloraxis.colorbar.title = '트렌드 강도'
    fig.write_image(f'{sectors}_search_trend.png')
    
    
if __name__ == "__main__":
    args = parser.parse_args()
    get_trend(args.sector, args.keywords, args.start_day, args.end_day)
        


