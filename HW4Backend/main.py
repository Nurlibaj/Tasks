from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.repository import BooksRepository

app = FastAPI()

templates = Jinja2Templates(directory="templates")
repository = BooksRepository()


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/books")
def get_books(request: Request,page:int | None = 1,  page_size:int | None = 10):
    books = repository.get_all()
    start = (page - 1) * page_size
    end = start + page_size

    prev = None
    if page > 1:
        prev = f"/books?page={page - 1}&page_size={page_size}"

    next = None
    if end < len(books):
        next = f"/books?page={page + 1}&page_size={page_size}"
    books=books[start:end]

    return templates.TemplateResponse(
        "books/index.html",
        {"request": request, "books": books, "prev": prev, "next": next},
    )
@app.get("/books/new")
def new_book(request: Request):
    return templates.TemplateResponse("books/new.html", {"request": request})
@app.get("/books/{book_id}")
def get_book(request: Request, book_id:int):
    book=repository.get_one(book_id)
    print(book)
    return templates.TemplateResponse("books/book_info.html",{"request":request,"book":book})




@app.post("/books")
async def add_book(request:Request,title:str=Form(...),author:str=Form(...),year:str=Form(...),total_pages:int=Form(...),genre:str=Form(...)):
    books=repository.get_all()
    id=len(books)+1
    book={"id":int(id),"title":title, "author":author,"year":int(year),"total_pages":int(total_pages),"genre":genre}
    repository.save(book)
    return RedirectResponse(url="/books",status_code=303)

