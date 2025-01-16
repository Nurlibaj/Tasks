from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from fastapi.requests import Request
from attrs import define
import csv
app = FastAPI()

templates = Jinja2Templates(directory="templates")
@define
class Comment:
    id:int
    text:str
    type:str
class  Repository:
    def __init__(self):
        self.comments = []
        with open('data.csv', "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                comment = Comment(
                    id=int(row["id"]),
                    text=row["text"],
                    type=row["type"]
                )

                self.comments.append(comment)
    def add_comment(self, text, type):
        new_comment = Comment(
            id=len(self.comments) + 1,
            text=text,
            type=type
        )
        self.comments.append(new_comment)
        with open("data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([new_comment.id, new_comment.text, new_comment.type])

    def get_comments(self):
        return self.comments
repo=Repository()
@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):

    comments = repo.get_comments()
    return templates.TemplateResponse("index.html", {"request": request, "comments": comments})
@app.get("/get_comments", response_class=HTMLResponse)
async def get_comments(request: Request):
    comments=repo.get_comments()
    return templates.TemplateResponse("index.html", {"request": request, "comments": comments})


@app.post("/add_comment")
async def submit_form(request:Request,text: str = Form(...), sellist1: str = Form(...)):
    repo.add_comment(text, sellist1)
    comments = repo.get_comments()
    return templates.TemplateResponse("index.html", {"request": request, "comments": comments})