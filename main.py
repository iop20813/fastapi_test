from fastapi import FastAPI,Query,Path
from typing import Annotated
from fastapi.responses import HTMLResponse,FileResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
app= FastAPI()

@app.get("/test")
def testGET():
    return {"date":10, "methon":"GET"}
@app.post("/test")
def testPOST():
    return {"date":True ,"methon":"POST"}

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