# %%
# %%
import sqlite3
import pandas as pd
from wordcloud import WordCloud
from collections import Counter

con = sqlite3.connect(r'.\bigkinds.db')

# %%
def get_wordcloud_newslist(target_date, keyword_list) :
    
    SQL = f'SELECT * FROM {target_date[0]}'
    df = pd.read_sql(SQL, con)
    for i in target_date[1:]:
        SQL = f'SELECT * FROM {i}'
        df_tmp = pd.read_sql(SQL, con)
        df = pd.concat([df, df_tmp])
    df.reset_index(drop=True, inplace=True)
    
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
    
    return img_wordcloud, news_list_df
    
if '__main__' == __name__:
    img_wordcloud, news_list_df = get_wordcloud_newslist(target_date=['d20220513','d20220516'], keyword_list=['마리화나','마이더스AI',''])
    img_wordcloud.to_file(r'.\wordcloud.png')
    news_list_df.to_csv(r'.\news_list.csv', index=False)
    con.close()



