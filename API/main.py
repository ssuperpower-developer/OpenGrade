# This Python file uses the following encoding: utf-8

from typing import Union,Optional
from fastapi import FastAPI
import requests
import get_grade
import parse
import insert_sql
from pydantic import BaseModel
import uvicorn



# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8080,host="0.0.0.0",workers=4, log-level="info")

class Item(BaseModel):
    id_: str
    passwd: str
    year: str
    semester: str

class Key(BaseModel):
    id_: str
    sToken: str

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello":"World"}


# @app.get("/token/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

#uvicorn main:app --host=0.0.0.0 --port=8080
@app.post("/grade/semester")
def get_token(item:Item):

    login_url = "https://smartid.ssu.ac.kr/Symtra_sso/smln_pcs.asp"
    user_data = {
        "userid": item.id_,
        "pwd": item.passwd
    }
    login_res = requests.post(login_url, data=user_data)
    token = login_res.cookies['sToken']
    saint=get_grade.Saint(token)
    saint._load_grade_page()

    page_res=saint._get_grade_page(item.year,item.semester)
    saint._close_connection()
    grade=parse.parse_grade(page_res)

    return grade

@app.post("/grade/year")
def get_token(token:Key):

    # login_url = "https://smartid.ssu.ac.kr/Symtra_sso/smln_pcs.asp"
    # user_data = {
    #     "userid": item.id_,
    #     "pwd": item.passwd
    # }
    # login_res = requests.post(login_url, data=user_data)
    # token = login_res.cookies['sToken']
    saint=get_grade.Saint(token.sToken)
    saint._load_grade_page()

    page_res_tuple=saint._get_grade_page_year()
    saint._close_connection()
    grade_first=parse.parse_grade(page_res_tuple[0])
    grade_second=parse.parse_grade(page_res_tuple[1])
    
    grade_first.extend(grade_second)


    subject_names = ['PHL', '융합전공을위한수학', '빅데이터프로그래밍언어',"IT기반의유통물류경영",'프로그래밍및실습']

    grade_infos = [grade for grade in grade_first if grade['과목명'] in subject_names] #배열안에 딕셔너리

    grade_simple=dict()
    for i in grade_infos:
        grade_simple[i["과목명"]]=i["성적"]
    
    #
        

    #예외처리 필요
    grade_simple["phl"]=grade_simple.pop("PHL")
    grade_simple["math"]=grade_simple.pop("융합전공을위한수학")
    grade_simple["programming"]=grade_simple.pop("프로그래밍및실습")
    grade_simple["business_management"]=grade_simple.pop("IT기반의유통물류경영")
    grade_simple["big_data"]=grade_simple.pop("빅데이터프로그래밍언어")

    # grade_simple["com_score"]=0.2*int(grade_simple["phl"])+0.2*int(grade_simple["math"])
    # +0.3*int(grade_simple["big_data"])+0.3*int(grade_simple["business_management"])
    # grade_simple["soft_score"]=0.2*int(grade_simple["phl"])+0.2*int(grade_simple["math"])
    # +0.3*int(grade_simple["big_data"])+0.3*int(grade_simple["programming"])

    # insert_sql()



    return grade_simple