from fastapi import FastAPI, HTTPException

# Importar nuestros módulos
from models import UserRegister, UserLogin, TokenVerify, UserResponse, LoginResponse, TokenResponse
from database import user_exists, create_user, get_user_by_username
from auth_utils import hash_password, verify_password, create_access_token, verify_token

app = FastAPI(title="Auth Service")

@app.post("/register", response_model=UserResponse)
def register(user_data: UserRegister):
    """Registrar un nuevo usuario"""
    # Verificar si el usuario ya existe
    if user_exists(user_data.username, user_data.email):
        raise HTTPException(400, "Usuario ya existe")
    
    # Crear usuario
    hashed_password = hash_password(user_data.password)
    new_user = create_user(user_data.username, user_data.email, hashed_password)
    
    return UserResponse(message="Usuario creado", user_id=new_user["id"])

@app.post("/login", response_model=LoginResponse)
def login(login_data: UserLogin):
    """Iniciar sesión y obtener token"""
    # Buscar usuario
    user = get_user_by_username(login_data.username)
    if not user:
        raise HTTPException(401, "Credenciales incorrectas")
    
    # Verificar contraseña
    if not verify_password(login_data.password, user["password"]):
        raise HTTPException(401, "Credenciales incorrectas")
    
    # Crear token
    access_token = create_access_token(user["username"], user["id"])
    
    return LoginResponse(
        access_token=access_token,
        user_id=user["id"],
        username=user["username"]
    )

@app.post("/verify", response_model=TokenResponse)
def verify_user_token(token_data: TokenVerify):
    """Verificar si un token es válido"""
    result = verify_token(token_data.token)
    
    if not result["valid"]:
        raise HTTPException(401, "Token inválido")
    
    return TokenResponse(
        valid=result["valid"],
        user=result["user"],
        user_id=result["user_id"]
    )

@app.get("/")
def health():
    """Endpoint de salud del servicio"""
    return {"service": "auth", "status": "ok"}