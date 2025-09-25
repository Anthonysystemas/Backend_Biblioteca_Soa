from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import httpx

# Importaciones locales
from models import CategoryCreate, BookCreate, BookUpdate, TokenVerify
from database import (
    get_categories, create_category, get_books, get_book_by_id, 
    create_book, update_book, category_exists
)
from config import APP_TITLE, SERVICE_NAME, AUTH_URL

app = FastAPI(title=APP_TITLE)

# Función para verificar token con el auth-service
async def verify_token(token: str) -> dict:
    """
    Verificar token con el servicio de autenticación
    """
    async with httpx.AsyncClient() as client:
        try:
            # Usar el modelo correcto que espera el auth-service
            token_data = TokenVerify(token=token)
            response = await client.post(f"{AUTH_URL}/verify", json=token_data.dict())
            
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Token inválido")
            
            return response.json()
            
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503, 
                detail=f"Auth service no disponible: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error verificando token: {str(e)}"
            )

# ========== CATEGORÍAS ==========
@app.get("/categories")
def get_all_categories():
    return get_categories()

@app.post("/categories")
async def create_new_category(category_data: CategoryCreate):
    await verify_token(category_data.token)  # Verificar autenticación
    
    return create_category(
        name=category_data.name,
        description=category_data.description
    )

# ========== LIBROS ==========
@app.get("/books")
def get_all_books(category_id: Optional[int] = Query(None)):
    return get_books(category_id)

@app.get("/books/{book_id}")
def get_single_book(book_id: int):
    book = get_book_by_id(book_id)
    
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    return book

@app.post("/books")
async def create_new_book(book_data: BookCreate):
    await verify_token(book_data.token)  # Verificar autenticación
    
    # Verificar que la categoría existe
    if not category_exists(book_data.category_id):
        raise HTTPException(status_code=400, detail="Categoría no existe")
    
    return create_book(
        title=book_data.title,
        author=book_data.author,
        isbn=book_data.isbn,
        price=book_data.price,
        category_id=book_data.category_id,
        description=book_data.description,
        available_copies=book_data.available_copies,
        total_copies=book_data.total_copies,
        publication_year=book_data.publication_year,
        publisher=book_data.publisher,
        format=book_data.format
    )

@app.put("/books/{book_id}")
async def update_existing_book(book_id: int, update_data: BookUpdate):
    await verify_token(update_data.token)
    
    # Preparar datos de actualización excluyendo el token
    update_dict = {
        "title": update_data.title,
        "author": update_data.author,
        "isbn": update_data.isbn,
        "price": update_data.price,
        "available_copies": update_data.available_copies,
        "total_copies": update_data.total_copies,
        "description": update_data.description
    }
    
    updated_book = update_book(book_id, update_dict)
    
    if not updated_book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    return updated_book

@app.get("/")
def health():
    return {"service": SERVICE_NAME, "status": "ok", "endpoints": ["categories", "books"]}