from fastapi import FastAPI,Query,Path,Body,Request
from typing import Annotated
from fastapi.responses import HTMLResponse,FileResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import json
import mysql.connector
from starlette.middleware.sessions import SessionMiddleware

# 定義請求模型
class MessageCreate(BaseModel):
    author: str
    content: str

# 定義響應模型
class MessageResponse(BaseModel):
    id: int
    author: str
    content: str
    created_at: datetime

app= FastAPI()
app.add_middleware(SessionMiddleware, secret_key="test20585")  # secret_key請自行設計

con = mysql.connector.connect(
    user = 'root',
    password='12395461',
    host = 'localhost',
    database = 'mydb'
)

@app.get("/hello")
def hello(request:Request,name):
    request.session['name'] = name
    return {"message": f"Hello, {name}!"}
@app.get("/talk")
def talk(request:Request):
    if 'name' in request.session:
        # 如果 session 中有 'name'，則使用它
        name = request.session['name']
        return {"message": f"Hello, {name} well comback!"}
    else:
        # 如果 session 中沒有 'name'，則返回一個提示
        return {"message": "Hello, please provide your name!"}
    
@app.post("/api/message", response_model=MessageResponse)
def createMessage(message: MessageCreate):
    cursor=con.cursor()    
    cursor.execute("INSERT INTO message(author,content) VALUES(%s,%s)",[message.author,message.content])
    con.commit()
    
    # 獲取新插入的記錄
    cursor.execute("SELECT * FROM message WHERE id = LAST_INSERT_ID()")
    new_message = cursor.fetchone()
    return {
        "id": new_message[0],
        "author": new_message[1],
        "content": new_message[2],
        "created_at": new_message[3]
    }

@app.get("/api/message", response_model=list[MessageResponse])
def get_message():
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM message")
    data = cursor.fetchall()
    # 將 create_time 映射到 created_at
    for item in data:
        item['created_at'] = item.pop('create_time')
    return data

@app.delete("/api/message/{id}")
def delet_message(id):
    cursor = con.cursor()
    cursor.execute("DELETE FROM message WHERE id=%s",[id])
    con.commit()
    return {"ok":True}

@app.get("/test")
def testGET():
    return {"date":10, "methon":"GET"}
@app.post("/add")
def testPOST(body=Body(None)):
    data = json.loads(body)
    print('data')
    print(data)
    result = data['n1']+data['n2']
    return {"date":True ,"methon":"POST","result":result}

def hello(name):
    message = "hi."+name
    return {"message":message}

@app.get("/multiply")
def multiplay(n1,n2):
    n1 = int(n1)
    n2 = int(n2)
    result = n1 * n2
    return {'result':result}
@app.get("/square")
def square(
    number:Annotated[int,None]
    ):
    number = int(number)
    return {'result':number*number}

@app.get("/mutiply")
def mutiply(n1:Annotated[int,None],n2:Annotated[int,None]):
    result = n1*n2
    return {"data":result}

@app.get("/items/")
def read_items(
    name: Annotated[str, Query(min_length=3, max_length=10)]
):
    return {"name": name}

@app.get("/hello")
def hello_(name:Annotated[str,Query(min_length=3)]):
    return {"message":"Hello"+name}

@app.get("/img/logo")
def logo():
    return FileResponse("123.jpg")
@app.get("/member")
def member():
    return RedirectResponse("https://www.google.com/")

app.mount( "/",StaticFiles(directory="public",html=True))

#uvicorn main:app --reload
# 外部訪問
#uvicorn main:app --host 0.0.0.0 --port 8000