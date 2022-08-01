
# 빅카인즈, 네이버 경제 뉴스와 키워드 수집 프로젝트  

## 개발 환경

### OS : Windows 10  
&nbsp;
### Browser : Chrome 103.0.5060.134(공식 빌드) (64비트)  
&nbsp;

### Python Version : 3.8.6  
&nbsp;
  

**기타 주요 라이브러리의 버전은 requirements.txt를 확인해주세요**  

&nbsp;

## Quick Guide
&nbsp;

PC에 깃이 설치되어 있을 경우 아래 코드를 cli에 입력  
`    
git clone https://github.com/dlfrnaos19/bigkinds_venv.git
`  
&nbsp;

클론폴더(bigkinds_venv)가 생성된 곳에 virtualenv 가상환경 생성  
`
virtualenv bigkinds_venv
`

&nbsp;

가상환경 실행  
`
[본인경로]\bigkinds_venv\Scripts\activate
`

&nbsp;

관련 라이브러리 설치

`
pip install -r requirements.txt
`

&nbsp;

데이터가 수집되어 있는 DB (DB내에서 날짜별 키워드 추출시 필요합니다)  
https://hycu-my.sharepoint.com/:f:/g/personal/g201915008_hycu_ac_kr/Epyx7gldXKFAvt1NKxieG2kB8cTKJKFkfhYaxQfFm6FGkQ?e=kFWZpq

&nbsp;

bigkinds.db : 19년도 까지 경제 뉴스데이터 수집  
bigkindsold.db : 15년도 까지 경제 뉴스데이터 수집  

**#get_wordcloud_newslist.py를 사용하려면 bigkinds_venv 폴더에에 db를 함께 넣어주세요**  

<details>
<summary>get_bigkinds_news 사용법</summary>

<div markdown="1">

1. bigkinds의 일자별 경제 기사를 셀레늄으로 검색하고, csv를 받는 과정에서 로그인이 필요하기 때문에, 로그인이 필요합니다.  

2. bigkinds_venv 경로내에 .env 파일을 만드시고, 안에 id = 아이디, pwd = 패스워드를 입력해주세요(환경변수를 통해 읽어옵니다)  
다운받은 excel 파일을 bigkinds.db에 'dYYYYMMDD'형태 테이블로 저장합니다. table이 존재하면 replace되니 주의하세요  
3. 다운 받은 excel 파일은 삭제합니다  
4. 스크립트의 실행  -s는 start day, -e는 end day 입니다  

&nbsp;

`
python get_bigkinds_news.py -s "YYYYMMDD" -e "YYYYMMDD"
`
</div>
</details>

&nbsp;

<details>
<summary> get_wordcloud_newslist 사용법</summary>

<div markdown="1">

1. 날짜와 키워드를 입력값으로 받아, db내에 해당 날짜를 검색해서 당일의 키워드로 워드클라우드를 생성하고, 해당 키워드가 존재하는 뉴스 기사 데이터프레임을 반환합니다
2. 실행하면 워드클라우드는 업종분야키워드_wordcloud.png, df는 업종분야키워드_news_list.csv생성
3. start_day와 end_day를 입력하면 날짜 리스트를 만들고 검색합니다.
4. keyword는 "마리화나,마이더스AI,아이유" 형식으로 입력받습니다
5. 키워드가 존재하지 않을 시 값이 없어 에러가 발생할 수 있습니다
6. 저장 외에 목적으로 사용할 경우, (워드클라우드, 뉴스리스트 dataframe) 형태 튜플로 반환합니다

`
python get_wordcloud_newslist_from_db.py -s "20220711" --e "20220715" -k "마리화나,마이더스AI,아이유"  
`

</div>
</details>

&nbsp;

<details>
<summary>get_navernews_by_date 사용법</summary>

<div markdown="1">

1. requests를 통해 네이버의 검색엔진에 해당 일자에 맞는 검색을 하고, 뉴스제목과 링크를 가져오며, 연관검색어가 있으면 같이 가져옵니다
2. 연관검색어는 나오기도, 안나오기도 합니다
3. get_naver_news_soup(검색시작날짜, 검색종료날짜, 키워드)를 입력하면 타이틀 리스트, 링크 리스트, 연관검색어 리스트가 csv파일로 저장됩니다
4. 함수로 사용하면, dataframe을 반환합니다

`
python get_navernews_by_date.py --start_day "20220711" --end_day "20220715" --keyword "아이유"  
`

</div>
</details>

&nbsp;

<details>
<summary> get_navertrend 사용법</summary>

<div markdown="1">

1. 업종과 키워드, 시작날짜와 마지막날짜를 입력값으로 받습니다
2. 반환값을 plotly로 그리고, html 파일로 저장합니다
3. 저장한 html 파일을 웹브라우저에서 열어보세요

`
python get_navertrend.py --sector "마리화나" --keywords "메디콕스,마이더스AI,아이큐어" --start_day "20220711" --end_day "20220715"
`

</div>
</details>

&nbsp;