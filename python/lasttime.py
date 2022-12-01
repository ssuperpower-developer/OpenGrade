from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager #크롬 웹 브라우저 자동 설치를 위한 라이브러리
from selenium.common.exceptions import StaleElementReferenceException

import datetime as dt
ser = Service("../chromedriver.exe")  # 크롬 드라이버 잡아주는 것
op = webdriver.ChromeOptions()  # initial
op.add_experimental_option("excludeSwitches", ["enable-logging"])  # option 주기
op.add_argument('--window-size=1920,1080')
op.add_argument("--headless") #CLI에서 실행
op.add_argument('--no-sandbox') #GPU관련 작업 하지 않음
op.add_argument('--disable-gpu') #GPU관련 작업 하지 않음
op.add_argument('--disable-dev-shm-usage') #공유 메모리 사용하지 않음, 속도 개선을 위해
op.add_argument("--disable-extensions") #크롬 확장 프로그램 사용하지 않음
op.add_argument('--blink-settings=imagesEnabled=false') #이미지 로딩하지 않음
# op.add_argument("headless")  # option 주기
prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
op.add_experimental_option('prefs', prefs)

start_time = time.perf_counter()

s = webdriver.Chrome(service=ser, options=op)  # 초기화


s.get("https://smartid.ssu.ac.kr/Symtra_sso/smln.asp?apiReturnUrl=https%3A%2F%2Fsaint.ssu.ac.kr%2FwebSSO%2Fsso.jsp")

ID = s.find_element(By.ID, "userid")
PWD = s.find_element(By.ID, "pwd")
LoginButton = s.find_element(By.CLASS_NAME, 'btn_login')

ID.send_keys("20213118")  # 학번
PWD.send_keys('rlagustn1!')  # 비밀번호
LoginButton.click()
# 학사관리 클릭
WebDriverWait(s,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#ddba4fb5fbc996006194d3c0c0aea5c4 > a"))).click()
#성적/졸업 클릭
WebDriverWait(s,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,r"#\38 d3da4feb86b681d72f267880ae8cef5 > a"))).click()
#닫기 창 누르기 위하여 iframe 바꾸기
WebDriverWait(s,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"URLSPW-0")))
#닫기 클릭
WebDriverWait(s,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#WD01C5"))).click()
#iframe 이동
WebDriverWait(s,10)
s.switch_to.parent_frame()
WebDriverWait(s,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"contentAreaFrame")))
WebDriverWait(s,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"isolatedWorkArea")))
#2021학년도 클릭 #WD011C-r  전체 ##WD011C-btn 버튼 
# WebDriverWait(s,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#WD011C-btn"))).click() #stale element reference: element is not attached to the page document
try:
    WebDriverWait(s,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#WD011C-btn"))).click() #stale element reference: element is not attached to the page document
except StaleElementReferenceException:
    WebDriverWait(s,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#WD011C-btn"))).click() #stale element reference: element is not attached to the page document
#2학기 클릭
WebDriverWait(s,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#WD0161"))).click() #이 부분 수정
#텍스트가 TBody에 들어올 때까지 대기
WebDriverWait(s,10).until(EC.text_to_be_present_in_element((By.ID,"WD0186-contentTBody"),"조회"))

html = s.page_source
soup = BeautifulSoup(html, 'html.parser')
tableitems = soup.find('tbody', {'id': "WD0186-contentTBody"})
soup = tableitems.find_all(
    'span', {"style": "white-space:normal;"})
scorelist = []
for i,v in enumerate(soup):
    if (i+1)%8:
        print(v.text ,end=" ")
    else:
        print(v.text)
end_time = time.perf_counter()

print('코드 실행 시간: %20ds' % (end_time - start_time))

# for index, value in enumerate(soup):
#     if (index % 8 == 0):
#         if (index == 0):
#             low = list()
#         else:
#             scorelist.append(low)
#             low = list()
#     else:
#         low.append(value.text)
# df = pd.DataFrame(scorelist, columns=[
#                   "이수학기", "과목코드", "과목명", "과목학점", "과목성적", "과목등급", "교수명"])
# print(df)
# df.to_excel("../result/practice.xlsx")
print(f"time elapsed : {int(round((end_time - start_time) * 1000))}ms")


#이게 리턴
# a = {"78910": {"등급": "A-", "성적": "90", "과목명": "플밍", "교수명": "김익수", "이수학점": "3"},
#      "123456": {"등급": "A+", "성적": "97", "과목명": "컴수", "교수명": "최종선", "이수학점": "3"}}

#이수학년도, 이수학기, 과목코드, 과목명, 과목학점, 성적(원점수), 등급, 교수명, 비고, 상세성적
