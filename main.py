from fastapi import FastAPI,Query,Path
from typing import Annotated
from fastapi.responses import HTMLResponse,FileResponse,RedirectResponse
app= FastAPI()

@app.get("/")
def index():
   # return {"data":"Home page"}
    return FileResponse('home.html')
@app.get("/hello1")
def hello(name):
    message = "hi."+name
    return {"message":message}

@app.get("/multiply")
def multiplay(n1,n2):
    n1 = int(n1)
    n2 = int(n2)
    result = n1 * n2
    return {'result':result}
@app.get("/square/{number}")
def square(
    number:Annotated[int,Path(gt=3,it=10)]
    ):
    number = int(number)
    return {'result':number*number}

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
#uvicorn main:app --reload