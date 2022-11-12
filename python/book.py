from bs4 import BeautifulSoup
import pandas as pd
html = open("../tableitems.html", "r+")
soup = BeautifulSoup(html, 'html.parser')

score = soup.find_all('span', {'style': 'white-space: normal'})
scorelist = []
for index, value in enumerate(score):
    if (index % 8 == 0):
        if(index == 0):
            low = list()
        else:
            scorelist.append(low)
            low = list()
    else:
        low.append(value.text)
df = pd.DataFrame(scorelist, columns=[
                  "이수학기", "과목코드", "과목명", "과목학점", "과목성적", "과목등급", "교수명"])

df.to_excel("./practice.xlsx")
