import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import http.client

start_time = time.perf_counter()

# print(datetime.today().weekday())
ary=[]
for i in range(12,17):
    if i<10:
        i=f"0{i}"
    ary.append(requests.get(f"http://m.soongguri.com/m_req/m_menu.php?rcd=1&sdt=202212{i}"))


for i in ary:
    soup = BeautifulSoup(i.text, "html.parser")
    project=soup.find(text="----------")
    학생식당메뉴=project.find_next()
    print(학생식당메뉴.text)

end_time = time.perf_counter()
print(f"time elapsed : {int(round((end_time - start_time) * 1000))}ms")


# for i in range(12,17):
#     r=requests.get(f"http://m.soongguri.com/m_req/m_menu.php?rcd=2&sdt=202212{i}")
#     soup = BeautifulSoup(r.text, "html.parser")
#     a=soup.find(text="----------")
#     b=a.find_next()
#     print(b.text)





