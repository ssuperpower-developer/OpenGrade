import time
import datetime
from bs4 import BeautifulSoup
import pandas as pd
html = open("../source/tableitems.html", "r+")
soup = BeautifulSoup(html, 'html.parser')
start = time.time()  # 시작


score = soup.find_all('span', {'style': 'white-space: normal'})
scorelist = []
for index, value in enumerate(score):
    if (index % 8 == 0):
        if (index == 0):
            low = list()
        else:
            scorelist.append(low)
            low = list()
    else:
        low.append(value.text)
df = pd.DataFrame(scorelist, columns=[
                  "이수학기", "과목코드", "과목명", "과목학점", "과목성적", "과목등급", "교수명", ])

print(df)

end = time.time()


sec = (end - start)
result = datetime.timedelta(seconds=sec)
print(result)
df.to_excel("../result/practice.xlsx")
