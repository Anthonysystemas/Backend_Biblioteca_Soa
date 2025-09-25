from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenVerify(BaseModel):
    token: str

class UserResponse(BaseModel):
    message: str
    user_id: int

class LoginResponse(BaseModel):
    access_token: str
    user_id: int
    username: str

class TokenResponse(BaseModel):
    valid: bool
    user: str
    user_id: int