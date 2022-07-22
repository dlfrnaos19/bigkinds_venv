# %%
# %%
import sqlite3
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
from tqdm import tqdm
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--start_day', type=int, default=20220513)
parser.add_argument('--end_day', type=int, default=20220714)
parser.add_argument('--keyword_list', type=str, default="마리화나,마이더스AI,아이유")

def get_wordcloud_newslist(start_day=20220513, end_day=20220714, keyword_list="마리화나,마이더스AI,아이유") :
    """_summary_

    Args:
        start_day (int, optional): _description_. Defaults to 20220513.
        end_day (int, optional): _description_. Defaults to 20220714.
        keyword_list (str, optional): column seperate로 입력해주세요. Defaults to "마리화나,마이더스AI,아이유".

    Returns:
        tuple: img_wordcloud[image], news_list_df[csv]
    """
    date_list = pd.date_range(str(start_day), str(end_day), freq='D').to_pydatetime().tolist()
    week_list = [date_list[i] for i in tqdm(range(len(date_list)),desc='create week list') if date_list[i].weekday() < 5]
    target_date = [i.strftime('d%Y%m%d') for i in tqdm(week_list,desc='convert week list to date')]
    print('week_date: 갯수', len(target_date))
    keyword_list = str(keyword_list).split(',')
    con = sqlite3.connect('bigkinds.db')
    
    SQL = f'SELECT * FROM {target_date[0]}'
    df = pd.read_sql(SQL, con)
    for i in target_date[1:]:
        SQL = f'SELECT * FROM {i}'
        df_tmp = pd.read_sql(SQL, con)
        df = pd.concat([df, df_tmp])
    df.reset_index(drop=True, inplace=True)
    con.close()
    # 특성추출에서 키워드 검색
    key_df = pd.DataFrame()
    for i in keyword_list:
        if df.본문.str.contains(i).sum():
            key_df = pd.concat([key_df,df[df['특성추출(가중치순 상위 50개)'].str.contains(i)]])    
    key_df.reset_index(drop=True, inplace=True)
    
    # 본문에서 키워드 검색 기능
    # key_df = pd.DataFrame()
    # for i in keywords:
    #     if df.본문.str.contains(i).sum():
    #         key_df = pd.concat([key_df,df[df['본문'].str.contains(i)]])    
    # key_df.reset_index(drop=True, inplace=True)
    news_list_df = key_df[['일자','본문','URL','특성추출(가중치순 상위 50개)']]
    key_list = news_list_df['특성추출(가중치순 상위 50개)'].to_list()
    
    # 문장 형태로 되어 있는 키워드 리스트를 1개의 리스트로 flatten
    gather_keyword = []
    for i in key_list:
        gather_keyword.extend(i.split(','))
        
        wordcloud = WordCloud(font_path='UttumDotumMR')
    counter_list = Counter(gather_keyword)
    img_wordcloud = wordcloud.generate_from_frequencies(counter_list)
    img_wordcloud.to_file(f'.\\{keyword_list[0]}_wordcloud.png')
    news_list_df.to_csv(f'.\\{keyword_list[0]}news_list.csv', index=False)
    
    return img_wordcloud, news_list_df
    
if '__main__' == __name__:
    args=parser.parse_args()
    img_wordcloud, news_list_df = get_wordcloud_newslist(args.start_day, args.end_day, args.keyword_list)
    



