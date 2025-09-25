from pydantic import BaseModel
from typing import Optional

# Modelos para categorías
class CategoryCreate(BaseModel):
    name: str
    description: str = ""
    token: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: str

# Modelos para libros
class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    price: float
    category_id: int
    description: str = ""
    available_copies: int = 1
    total_copies: int = 1
    publication_year: int
    publisher: str = ""
    format: str = "digital"
    token: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    price: Optional[float] = None
    available_copies: Optional[int] = None
    total_copies: Optional[int] = None
    description: Optional[str] = None
    token: str

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    description: str
    price: float
    category_id: int
    available_copies: int
    total_copies: int
    publication_year: int
    publisher: str
    format: str
    created_at: str
    updated_at: Optional[str] = None

# Modelo para verificación de token
class TokenVerify(BaseModel):
    token: str