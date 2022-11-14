from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
ser = Service("C:/Users/rover0811/chromedriver.exe")  # 크롬 드라이버 잡아주는 것
option = webdriver.ChromeOptions()  # initial
option.add_experimental_option(
    "excludeSwitches", ["enable-logging"])  # option 주기
option.add_argument('--window-size=1920,1080')
# option.add_argument("headless")  # option 주기
sel = webdriver.Chrome(service=ser, options=option)  # 초기화

sel.get("https://smartid.ssu.ac.kr/Symtra_sso/smln.asp?apiReturnUrl=https%3A%2F%2Fsaint.ssu.ac.kr%2FwebSSO%2Fsso.jsp")
