import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from config import CATEGORIES_FILE, BOOKS_FILE

def load_data(filename: str) -> List[Dict[str, Any]]:
    """Cargar datos desde archivo JSON"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(filename: str, data: List[Dict[str, Any]]) -> None:
    """Guardar datos a archivo JSON"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ========== CATEGORÍAS ==========
def get_categories() -> List[Dict[str, Any]]:
    """Obtener todas las categorías"""
    return load_data(CATEGORIES_FILE)

def create_category(name: str, description: str = "") -> Dict[str, Any]:
    """Crear nueva categoría"""
    categories = load_data(CATEGORIES_FILE)
    category_id = len(categories) + 1
    
    new_category = {
        "id": category_id,
        "name": name,
        "description": description,
        "created_at": datetime.now().isoformat()
    }
    
    categories.append(new_category)
    save_data(CATEGORIES_FILE, categories)
    
    return new_category

# ========== LIBROS ==========
def get_books(category_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Obtener todos los libros, opcionalmente filtrados por categoría"""
    books = load_data(BOOKS_FILE)
    
    if category_id:
        books = [b for b in books if b.get("category_id") == category_id]
    
    return books

def get_book_by_id(book_id: int) -> Optional[Dict[str, Any]]:
    """Obtener libro por ID"""
    books = load_data(BOOKS_FILE)
    
    for book in books:
        if book["id"] == book_id:
            return book
    
    return None

def category_exists(category_id: int) -> bool:
    """Verificar si una categoría existe"""
    categories = load_data(CATEGORIES_FILE)
    return any(c["id"] == category_id for c in categories)

def create_book(
    title: str,
    author: str,
    isbn: str,
    price: float,
    category_id: int,
    description: str = "",
    available_copies: int = 1,
    total_copies: int = 1,
    publication_year: int = 2024,
    publisher: str = "",
    format: str = "digital"
) -> Dict[str, Any]:
    """Crear nuevo libro"""
    books = load_data(BOOKS_FILE)
    book_id = len(books) + 1
    
    new_book = {
        "id": book_id,
        "title": title,
        "author": author,
        "isbn": isbn,
        "description": description,
        "price": price,
        "category_id": category_id,
        "available_copies": available_copies,
        "total_copies": total_copies,
        "publication_year": publication_year,
        "publisher": publisher,
        "format": format,
        "created_at": datetime.now().isoformat()
    }
    
    books.append(new_book)
    save_data(BOOKS_FILE, books)
    
    return new_book

def update_book(book_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Actualizar libro por ID"""
    books = load_data(BOOKS_FILE)
    
    for i, book in enumerate(books):
        if book["id"] == book_id:
            # Actualizar solo campos proporcionados
            if "title" in update_data and update_data["title"]:
                book["title"] = update_data["title"]
            if "author" in update_data and update_data["author"]:
                book["author"] = update_data["author"]
            if "isbn" in update_data and update_data["isbn"]:
                book["isbn"] = update_data["isbn"]
            if "price" in update_data and update_data["price"] is not None:
                book["price"] = update_data["price"]
            if "available_copies" in update_data and update_data["available_copies"] is not None:
                book["available_copies"] = update_data["available_copies"]
            if "total_copies" in update_data and update_data["total_copies"] is not None:
                book["total_copies"] = update_data["total_copies"]
            if "description" in update_data and update_data["description"]:
                book["description"] = update_data["description"]
            
            book["updated_at"] = datetime.now().isoformat()
            
            save_data(BOOKS_FILE, books)
            return book
    
    return None