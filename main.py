from fastapi import FastAPI,Query,Path
from typing import Annotated
app= FastAPI()

@app.get("/")
def index():
    return {"data":"Home page"}
@app.get("/hello")
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
#uvicorn main:app --reload