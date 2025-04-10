from fastapi import FastAPI,Query,Path,Body
from typing import Annotated
from fastapi.responses import HTMLResponse,FileResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
import json
import mysql.connector
app= FastAPI()
con = mysql.connector.connect(
    user = 'root',
    password='12395461',
    host = 'localhost',
    database = 'mydb'
)
@app.post("/api/message")
def createMessage(body=Body(None)):
    body=json.loads(body)
    author=body["author"]
    content=body["content"]
    cursor=con.cursor()    
    cursor.execute("INSERT INTO message(author,content) VALUES(%s,%s)",[author,content])
    con.commit()
    return{"ok":True}

@app.get("/api/message")
def get_message():
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT*FROM message")
    data = cursor.fetchall()
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