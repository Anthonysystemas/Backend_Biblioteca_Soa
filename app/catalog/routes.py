from flask import Blueprint, request
from ..common.models import Book

bp = Blueprint("catalog", __name__)

@bp.get("/books")
def list_books():
    q = request.args.get("q", "")
    query = Book.query
    if q:
        like = f"%{q}%"
        query = query.filter((Book.title.ilike(like)) | (Book.author.ilike(like)) | (Book.isbn.ilike(like)))
    books = query.limit(100).all()
    return [{
        "id": b.id, "isbn": b.isbn, "title": b.title, "author": b.author,
        "available_copies": b.available_copies
    } for b in books]
