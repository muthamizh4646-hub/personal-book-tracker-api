# Personal Book Tracker API

A simple FastAPI project to manage personal books using SQLite and SQLAlchemy.

## Features

- Add a new book
- View all books
- View one book by ID
- Update book status
- Delete a book
- Prevent duplicate books
- Search books by title or author
- Filter books by status
- Pagination support
- Alembic migration setup

## Technologies Used

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- Alembic
- Uvicorn

## Project Structure

```text
personal_book_tracker/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── alembic.ini
├── migrations/
└── README.md
