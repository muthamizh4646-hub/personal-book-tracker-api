'''
1.Add book
2. View all books
3. View one book
4. Update book status
5. Delete book
'''
from fastapi import FastAPI, HTTPException, Depends, Query
from enum import Enum
from sqlalchemy.orm import Session
from sqlalchemy import or_
import schemas
import models 
from database import engine,SessionLocal
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()
        
class Book_status(str,Enum):
    unread="unread"
    reading="reading"
    completed="completed"


@app.get("/")
def home():
    return {"message":"Welcome to Personal Book Tracker API"}

@app.post("/books", response_model=schemas.BookResponse)
def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    existing_book = (db.query(models.Book).filter( models.Book.title == book.title,models.Book.author == book.author).first())
    if existing_book is not None:
        raise HTTPException(status_code=409,
            detail="Book already exists")
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books", response_model=schemas.BookListResponse)
def get_all_books(
    status: schemas.BookStatus | None = None,
    search: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.Book)

    if status is not None:
        query = query.filter(
            models.Book.status == status.value
        )

    if search:
        query = query.filter(
            or_(
                models.Book.title.ilike(f"%{search}%"),
                models.Book.author.ilike(f"%{search}%")
            )
        )

    total = query.count()

    books = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "books": books
    }      


@app.get("/books/{book_id}",response_model=schemas.BookResponse)
def get_one_book(book_id:int,db:Session=Depends(get_db)):
    book = (db.query(models.Book).filter(models.Book.id == book_id).first())
    if book is None :
        raise HTTPException(status_code=404,detail="Book not found")
    return book


@app.patch("/books/{book_id}",response_model =schemas.BookResponse)
def update_book_status( book_id:int,status:Book_status ,db:Session = Depends(get_db)):
    book = (db.query(models.Book).filter(models.Book.id == book_id).first())
    if book is None :
        raise HTTPException(status_code=404,detail="Book not found")
    book.status = status.value
    db.commit()
    db.refresh(book)
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id:int,db:Session = Depends(get_db)):
    book = (db.query(models.Book).filter(models.Book.id == book_id).first())
    if book is None:
        raise HTTPException(status_code=404,detail="Book not found")
    db.delete(book) 
    db.commit()
    return {"message":"book deleted successfully"}   
