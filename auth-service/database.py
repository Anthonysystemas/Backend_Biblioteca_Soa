import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from config import USERS_FILE

def load_users() -> List[Dict[str, Any]]:
    """Cargar usuarios desde el archivo JSON"""
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_users(users: List[Dict[str, Any]]) -> None:
    """Guardar usuarios en el archivo JSON"""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Buscar usuario por nombre de usuario"""
    users = load_users()
    for user in users:
        if user["username"] == username:
            return user
    return None

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Buscar usuario por email"""
    users = load_users()
    for user in users:
        if user["email"] == email:
            return user
    return None

def user_exists(username: str, email: str) -> bool:
    """Verificar si ya existe un usuario con el mismo username o email"""
    return get_user_by_username(username) is not None or get_user_by_email(email) is not None

def create_user(username: str, email: str, hashed_password: str) -> Dict[str, Any]:
    """Crear un nuevo usuario"""
    users = load_users()
    user_id = len(users) + 1
    
    new_user = {
        "id": user_id,
        "username": username,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.now().isoformat()
    }
    
    users.append(new_user)
    save_users(users)
    
    return new_user