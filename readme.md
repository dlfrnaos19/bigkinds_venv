
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
https://drive.google.com/drive/folders/10s3fONH2pxjhc9yodMM_TEKaDwBftvsP?usp=sharing  

&nbsp;

bigkinds.db : 19년도 까지 경제 뉴스데이터 수집  
bigkindsold.db : 15년도 까지 경제 뉴스데이터 수집  

**#get_wordcloud_newslist.py를 사용하려면 bigkinds/data에 db를 넣어주세요**  

<details>
<summary>get_bigkinds_news 사용법</summary>

<div markdown="1">

1. bigkinds의 일자별 경제 기사를 셀레늄으로 검색하고, csv를 받는 과정에서 로그인이 필요하기 때문에, 로그인이 필요합니다.  

2. bigkinds경로내에 .env 파일을 만드시고, 안에 id = 아이디, pwd = 패스워드를 입력해주세요(환경변수를 통해 읽어옵니다)  
다운받은 excel 파일을 bigkinds.db에 'dYYYYMMDD'형태 테이블로 저장합니다. table이 존재하면 replace되니 주의하세요  
3. 다운 받은 excel 파일은 삭제합니다  
4. 스크립트의 실행  -s는 start day, -e는 end day 입니다  

&nbsp;

`
python get_bigkinds_news.py -s YYYYMMDD -e YYYYMMDD  
`
</div>
</details>

&nbsp;

<details>
<summary>get_wordcloud_newslist 사용법</summary>

<div markdown="1">

1. 날짜와 키워드를 입력값으로 받아, db내에 해당 날짜를 검색해서 당일의 키워드로 워드클라우드를 생성하고, 해당 키워드가 존재하는 뉴스 기사 데이터프레임을 반환합니다
2. 실행하면 워드클라우드는 wordcloud.png, df는 news_list.csv생성
3. 날짜와 키워드는 길이 2이상의 iterable한 객체가 필요합니다
4. 키워드가 존재하지 않을 시 값이 없어 에러가 발생할 수 있습니다
5. 입력값 2가지 target_date, keyword_list를 넣고 get_wordcloud_newslist를 호출하면 wordcloud, news_list_df 객체가 튜플로 반환되는데, 이때 워드클라우드의 이미지를 보려면 wordcloud.to_image()를, 저장하려면 to_file(파일명)을 작성하면 됩니다. news_list_df는 저장하려면 news_list_df.to_csv(파일명,index=False)로 하면 되겠습니다.  

</div>
</details>

&nbsp;

<details>
<summary>get_navernews_by_date 사용법</summary>

<div markdown="1">

1. requests를 통해 네이버의 검색엔진에 해당 일자에 맞는 검색을 하고, 뉴스제목과 링크를 가져오며, 연관검색어가 있으면 같이 가져옵니다
2. 연관검색어는 나오기도, 안나오기도 합니다
3. get_naver_news_soup(검색시작날짜, 검색종료날짜, 키워드)를 입력하면 타이틀 리스트, 링크 리스트, 연관검색어 리스트가 튜플로 반환됩니다

</div>
</details>