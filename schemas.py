from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class BookStatus(str, Enum):
    unread = "unread"
    reading = "reading"
    completed = "completed"


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    status: BookStatus = BookStatus.unread


class BookResponse(BookCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class BookListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    books: list[BookResponse]