from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time

ser = Service("C:/Users/rover0811/chromedriver.exe")  # 크롬 드라이버 잡아주는 것
op = webdriver.ChromeOptions()  # initial
op.add_experimental_option("excludeSwitches", ["enable-logging"])  # option 주기
# op.add_argument("headless")  # option 주기
s = webdriver.Chrome(service=ser, options=op)  # 초기화

s.get("http://m.soongguri.com/")

time.sleep(3)

html = s.page_source
soup = BeautifulSoup(html, 'html.parser')
items = soup.select(
    '#mainDiv > table > tbody > tr:nth-child(2) > td.menu_list>div')
container = []
for i in items:
    container.append(i.text)

Button = s.find_element(By.NAME, "rest")
도담 = s.find_element(
    By.CSS_SELECTOR, "#smenu1 > div:nth-child(1) > div > div > select > option:nth-child(2)")
Button.click()
도담.click()

time.sleep(3)
html = s.page_source

도담soup = BeautifulSoup(html, 'html.parser')
도담items = 도담soup.select(
    '#mainDiv > table > tbody > tr:nth-child(2) > td.menu_list>div')
# mainDiv > table > tbody > tr:nth-child(2) > td.menu_list > div:nth-child(1)
for i in 도담items:
    container.append(i.text)
for i in container:
    print(i)
# print(container)
time.sleep(20)  # 추후 명시적 대기로 바꾸어야 함
