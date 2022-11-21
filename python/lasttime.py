from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
import datetime as dt
ser = Service("C:/Users/rover0811/chromedriver.exe")  # 크롬 드라이버 잡아주는 것
op = webdriver.ChromeOptions()  # initial
op.add_experimental_option("excludeSwitches", ["enable-logging"])  # option 주기
op.add_argument('--window-size=1920,1080')
op.add_argument("headless")  # option 주기
s = webdriver.Chrome(service=ser, options=op)  # 초기화


s.get("https://smartid.ssu.ac.kr/Symtra_sso/smln.asp?apiReturnUrl=https%3A%2F%2Fsaint.ssu.ac.kr%2FwebSSO%2Fsso.jsp")

ID = s.find_element(By.ID, "userid")
PWD = s.find_element(By.ID, "pwd")
LoginButton = s.find_element(By.CLASS_NAME, 'btn_login')

ID.send_keys("비밀입니당")  # 학번
PWD.send_keys('비밀이에염')  # 비밀번호
LoginButton.click()

time.sleep(3)

학사관리Button = s.find_element(
    By.CSS_SELECTOR, "#ddba4fb5fbc996006194d3c0c0aea5c4 > a")

학사관리Button.click()

time.sleep(3)

성적졸업Button = s.find_element(
    By.CSS_SELECTOR, r"#\38 d3da4feb86b681d72f267880ae8cef5 > a")

성적졸업Button.click()

time.sleep(3)

s.switch_to.frame("URLSPW-0")
time.sleep(2)

s.find_element(By.CSS_SELECTOR, "#WD01C5").click()  # 여기서 에러가 나네?? 계절학기 이슈

time.sleep(3)
s.switch_to.parent_frame()

s.switch_to.frame("contentAreaFrame")
s.switch_to.frame("isolatedWorkArea")
s.find_element(By.CSS_SELECTOR, "#WD011C-btn").click()
s.find_element(By.CSS_SELECTOR, "#WD0161").click()  # 여기까지가 접근부

time.sleep(3)
html = s.page_source

soup = BeautifulSoup(html, 'html.parser')

tableitems = soup.find('tbody', {'id': "WD0186-contentTBody"})
print(type(tableitems))
print(tableitems)

soup = tableitems.find_all(
    'span', {"style": "white-space:normal;"})

scorelist = []
for index, value in enumerate(soup):
    if (index % 8 == 0):
        if (index == 0):
            low = list()
        else:
            scorelist.append(low)
            low = list()
    else:
        low.append(value.text)
df = pd.DataFrame(scorelist, columns=[
                  "이수학기", "과목코드", "과목명", "과목학점", "과목성적", "과목등급", "교수명"])

df.to_excel("../result/practice.xlsx")

# tableitems = tableitems[0].find_all('span', {'style': 'white-space: normal'})
