from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import os 
import time
import sqlite3
import re
import argparse
from dotenv import load_dotenv

import pandas as pd
from tqdm import tqdm

parser = argparse.ArgumentParser(description='사용')
parser.add_argument('-s','--start_day', type=int, default=20200101, help='크롤링 시작할 날짜 yyyymmdd')
parser.add_argument('-e','--end_day', type=int, default=20220714, help='크롤링 종료할 날짜 yyyymmdd')
args = parser.parse_args()

def get_webdriver():
    options = webdriver.ChromeOptions()
    header = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'
    options.add_argument('window-size=1280x1080') # 

    options.add_argument(header)
    path = r'.\chromedriver.exe'
    print('driver loading...')
    return webdriver.Chrome(path, options=options)

def get_week_date(start_day=20200101, end_day=20220714):
    date_list = pd.date_range(str(start_day), str(end_day), freq='D').to_pydatetime().tolist()
    week_list = [date_list[i] for i in tqdm(range(len(date_list)),desc='create week list') if date_list[i].weekday() < 5]
    week_date = [i.strftime('%Y-%m-%d') for i in tqdm(week_list,desc='convert week list to date')]
    print('week_date:', week_date)
    return week_date

def get_login_driver(driver):
    # load .env
    load_dotenv()
    
    # 메인페이지 로그인
    driver.get('https://www.bigkinds.or.kr')
    time.sleep(2)
    menu_button_path = driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/button')
    menu_button_path.click()
    time.sleep(1)
    login_button_path = driver.find_element(By.XPATH,'//*[@id="header"]/div[2]/div[1]/button[2]')
    login_button_path.click()
    time.sleep(1)
    kinds_login_id_path = driver.find_element(By.XPATH, '//*[@id="login-user-id"]')
    kinds_login_id_path.send_keys(os.environ['id'])
    time.sleep(0.5)
    kinds_login_pwd_path = driver.find_element(By.XPATH, '//*[@id="login-user-password"]')
    kinds_login_pwd_path.send_keys(os.environ['pwd'])
    time.sleep(0.5)
    login_button_path = driver.find_element(By.XPATH, '//*[@id="login-btn"]')
    login_button_path.click()
    print('login success')
    return driver

def get_date_table(date):
    days_button_path = driver.find_element(By.XPATH, '//*[@id="collapse-step-1-body"]/div[3]/div/div[1]/div[1]/a')
    days_button_path.click()
    time.sleep(0.5)
    one_day_xpath = driver.find_element(By.XPATH, '//*[@id="srch-tab1"]/div/div[1]/span[1]/label')
    one_day_xpath.click()
    # 기간 설정
    start_day_xpath = driver.find_element(By.XPATH, '//*[@id="search-begin-date"]')
    start_day_xpath.click()
    time.sleep(0.5)
    for i in range(10):
        start_day_xpath.send_keys(Keys.BACK_SPACE)
    start_day_xpath.send_keys(date)
    time.sleep(0.5)
    end_day_xpath = driver.find_element(By.XPATH, '//*[@id="search-end-date"]')
    end_day_xpath.click()
    for i in range(10):
        end_day_xpath.send_keys(Keys.BACK_SPACE)
    end_day_xpath.send_keys(date)
    print("기간 설정 완료")
    time.sleep(0.5)

    # 언론사 설정
    media_xpath = driver.find_element(By.XPATH, '//*[@id="collapse-step-1-body"]/div[3]/div/div[1]/div[3]/a')
    media_xpath.click()
    time.sleep(0.3)
    # 경제 일간지 클릭
    economy_button_path = driver.find_element(By.XPATH, '//*[@id="category_provider_group"]/li[2]/span')
    economy_button_path.click()
    time.sleep(0.3)
    # 통합 분류 설정
    topic_button_path = driver.find_element(By.XPATH, '//*[@id="collapse-step-1-body"]/div[3]/div/div[2]/div[1]/a')
    topic_button_path.click()
    time.sleep(0.3)
    # 통합 분류 체크박스
    topic_checkbox_path = driver.find_element(By.XPATH, '//*[@id="srch-tab3"]/ul/li[2]/div/span[3]/label/span')
    topic_checkbox_path.click()
    time.sleep(0.3)
    # 검색 적용하기 클릭
    search_button_path = driver.find_element(By.XPATH, '//*[@id="search-foot-div"]/div[2]/button[2]')
    search_button_path.click()
    print('검색 중...')
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.3)
    # 분석 결과 및 시각화 버튼
    anal_result_button_path = driver.find_element(By.XPATH, '//*[@id="collapse-step-3"]')
    anal_result_button_path.click()
    time.sleep(1)
    # 엑셀 다운로드 버튼
    down_excel_path = driver.find_element(By.XPATH, '//*[@id="analytics-data-download"]/div[3]/button')
    down_excel_path.click()
    print('다운로드 중...', date)
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(9)
    
    only_num = re.sub(r'[^0-9]', '', date)
    # download_path = 크롬의 파일 기본 저장 경로
    download_path = os.path.join(r"C:\Users", os.getlogin()+r"\Downloads")
    file_path = os.path.join(download_path,f'NewsResult_{only_num}-{only_num}.xlsx')
    df = pd.read_excel(file_path, engine='openpyxl')
    con = sqlite3.connect('./data/bigkinds.db')
    df.to_sql('d'+only_num, con, if_exists='replace', index=False)
    print('Table 저장 완료')
    os.remove(file_path)
    print('파일 삭제 완료')

if __name__ == '__main__':
    main_url = 'https://www.bigkinds.or.kr/'
    search_url = 'https://www.bigkinds.or.kr/v2/news/index.do'
    driver = get_webdriver()
    time.sleep(0.5)
    driver.get('https://naver.com')
    time.sleep(2)
    driver = get_login_driver(driver)
    time.sleep(1)
    
    start_day = args.start_day
    end_day = args.end_day
    week_date = get_week_date(start_day, end_day)
    for date in tqdm(week_date):
        driver.get(search_url)
        time.sleep(2)
        get_date_table(date)
    driver.quit()