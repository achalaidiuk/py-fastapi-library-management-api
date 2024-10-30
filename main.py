from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas

from db.database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{id}/", response_model=schemas.Author)
def get_author_by_id(
        id: int,
        db: Session = Depends(get_db),
):
    author = crud.get_author_by_id(db=db, id=id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/{id}/", response_model=schemas.Book)
def get_book_by_id(id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db=db, id=id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


@app.get("/books/", response_model=list[schemas.Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=skip, limit=limit)
