import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# ser = Service("C:/Users/rover0811/chromedriver.exe")  # 크롬 드라이버 잡아주는 것
# op = webdriver.ChromeOptions()  # initial
# op.add_experimental_option("excludeSwitches", ["enable-logging"])  # option 주기
# op.add_argument('--window-size=1920,1080')
# s = webdriver.Chrome(service=ser, options=op)  # 초기화


#유세인트 초기 로그인 api
login_url = "https://smartid.ssu.ac.kr/Symtra_sso/smln_pcs.asp"
user_agent = ""

user_data = {
    "in_tp_bit": "0",
    "rqst_caus_cd": "03",
    "userid": "",
    "pwd": ""
}

header = {
    "referer": login_url,
    "user-agent": user_agent
}

session = requests.Session()

with session as s:
    s.post(login_url, headers=header, data=user_data)
    login_cookies = requests.utils.dict_from_cookiejar(s.cookies)
    session_token = login_cookies['sToken']

    #여기에 전달 받은 토큰을 넘겨주면 세션이 생성됨
    pass_token_url = f"https://saint.ssu.ac.kr/webSSO/sso.jsp?sToken={session_token}"
    
    s.get(pass_token_url, headers=header)
    header["referer"] = pass_token_url

		#세션을 통해 유세인트 접근하면 접속 성공    
    res = s.get("https://saint.ssu.ac.kr/irj/portal", headers=header)
    print(res.text)