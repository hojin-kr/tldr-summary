from typing import Union

from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from typing import List
from textrankr import TextRank
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class Summary(BaseModel):
    input: str
    output: str
    grade: int

class Tokenizer:
    def __call__(self, text: str) -> List[str]:
        tokens: List[str] = text.split()
        return tokens

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(date + ' ' + message + "\n")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.put("/summary")
def update_summarizer(summary: Summary, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "summary")
    mytokenizer: Tokenizer = Tokenizer()
    textrank: TextRank = TextRank(mytokenizer)
    k: int = summary.grade  # num sentences in the resulting summary
    summary.output: str = textrank.summarize(summary.input, k)
    return {"input": summary.input, "output": summary.output, "garde": summary.grade}
