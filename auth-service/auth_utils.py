from datetime import datetime, timedelta
from jose import jwt
from config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_HOURS, pwd_context

def hash_password(password: str) -> str:
    """Hashear una contraseña"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar una contraseña contra su hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(username: str, user_id: int) -> str:
    """Crear un token JWT"""
    expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    token_data = {
        "sub": username, 
        "user_id": user_id, 
        "exp": expire
    }
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    """Verificar y decodificar un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "valid": True,
            "user": payload["sub"],
            "user_id": payload.get("user_id"),
            "payload": payload
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }